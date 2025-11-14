use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use scraper::{Html, Selector};
use reqwest;
use futures::future::join_all;
use std::sync::Arc;
use tokio::sync::Semaphore;
use std::time::{Duration, Instant};

#[global_allocator]
static GLOBAL: mimalloc::MiMalloc = mimalloc::MiMalloc;

async fn fetch_and_parse(client: &reqwest::Client, url: String, selector_str: String) -> Result<(Vec<String>, Duration), String> {
    let start_time = Instant::now();
    let response = client.get(&url).send().await.map_err(|e| e.to_string())?;
    let bytes = response.bytes().await.map_err(|e| e.to_string())?;
    let body = String::from_utf8_lossy(&bytes).to_string();
    
    let result = tokio::task::spawn_blocking(move || {
        let fragment = Html::parse_document(&body);
        let sel = Selector::parse(&selector_str).unwrap();
        fragment.select(&sel)
            .map(|element| element.text().collect::<String>())
            .collect()
    }).await.unwrap();

    Ok((result, start_time.elapsed()))
}

async fn scrape_all_urls(urls: Vec<String>, selector: String, concurrency: usize) -> PyResult<(Vec<Vec<String>>, Vec<u64>)> {
    let client = reqwest::Client::builder()
        .tcp_nodelay(true)
        .timeout(Duration::from_millis(500)) // Relaxed timeout
        .connect_timeout(Duration::from_millis(250)) // Relaxed connect timeout
        .build()
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;

    let semaphore = Arc::new(Semaphore::new(concurrency));
    
    let futures = urls.into_iter().map(|url| {
        let client = client.clone();
        let selector = selector.clone();
        let semaphore = semaphore.clone();
        
        tokio::spawn(async move {
            let _permit = semaphore.acquire().await.unwrap();
            fetch_and_parse(&client, url, selector).await
        })
    });

    let task_results = join_all(futures).await;

    let mut final_results = Vec::new();
    let mut latencies_ms = Vec::new();
    for task_result in task_results {
        match task_result {
            Ok(Ok((elements, duration))) => {
                final_results.push(elements);
                latencies_ms.push(duration.as_millis() as u64);
            },
            Ok(Err(e)) => return Err(pyo3::exceptions::PyConnectionError::new_err(e)),
            Err(e) => return Err(pyo3::exceptions::PyRuntimeError::new_err(e.to_string())),
        }
    }

    Ok((final_results, latencies_ms))
}

#[pyfunction]
fn scrape_urls_concurrent(py: Python, urls: Vec<String>, selector: String, concurrency: usize) -> PyResult<&PyAny> {
    pyo3_asyncio::tokio::future_into_py(py, async move {
        scrape_all_urls(urls, selector, concurrency).await
    })
}

#[pymodule]
fn rust_scraper(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(scrape_urls_concurrent, m)?)?;
    Ok(())
}

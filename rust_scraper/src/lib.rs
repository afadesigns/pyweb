//! The high-performance, asynchronous Rust core for the `pyweb` web scraper.
//!
//! This module provides the core scraping functionality, heavily optimized for speed.
//! It leverages `tokio` for asynchronous I/O, `reqwest` for a robust HTTP client,
//! `scraper` for efficient HTML parsing, and `mimalloc` for a high-performance memory allocator.

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

/// Fetches the content of a single URL, parses it with the provided CSS selector,
/// and returns the extracted text elements and the total time elapsed for the operation.
///
/// This function is the core of the concurrent scraping process.
///
/// # Arguments
///
/// * `client` - A reference to the shared `reqwest::Client`.
/// * `url` - The URL to fetch.
/// * `selector` - An `Arc<Selector>` containing the pre-parsed CSS selector to apply.
///
/// # Returns
///
/// A `Result` containing a tuple of `(Vec<String>, Duration)` on success, or a `String` error on failure.
async fn fetch_and_parse(client: &reqwest::Client, url: String, selector: Arc<Selector>) -> Result<(Vec<String>, Duration), String> {
    let start_time = Instant::now();
    let response = client.get(&url).send().await.map_err(|e| e.to_string())?;
    let bytes = response.bytes().await.map_err(|e| e.to_string())?;
    let body = String::from_utf8_lossy(&bytes).into_owned();

    // The parsing logic is CPU-bound, so we move it to a blocking thread
    // to avoid stalling the async runtime.
    let result = tokio::task::spawn_blocking(move || {
        let fragment = Html::parse_document(&body);
        fragment.select(&selector)
            .map(|element| element.text().collect::<String>())
            .collect()
    }).await.unwrap();

    Ok((result, start_time.elapsed()))
}

/// Scrapes a list of URLs concurrently with a shared `reqwest` client and a semaphore for concurrency control.
///
/// This is the main entry point for the scraping logic. It sets up the client, parses the selector once,
/// and then spawns a Tokio task for each URL.
///
/// # Arguments
///
/// * `urls` - A `Vec<String>` of URLs to scrape.
/// * `selector_str` - The CSS selector string to apply to each page.
/// * `concurrency` - The maximum number of concurrent requests.
///
/// # Returns
///
/// A `PyResult` containing a tuple of `(Vec<Vec<String>>, Vec<u64>)` on success, where the first element
/// is a list of scraped results for each URL, and the second is a list of latencies in milliseconds.
async fn scrape_all_urls(urls: Vec<String>, selector_str: String, concurrency: usize) -> PyResult<(Vec<Vec<String>>, Vec<u64>)> {
    let client = reqwest::Client::builder()
        .http1_only()
        .tcp_nodelay(true)
        .timeout(Duration::from_millis(500))
        .connect_timeout(Duration::from_millis(250))
        .build()
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;

    // --- OPTIMIZATION: Parse selector once and share it ---
    let selector = Arc::new(Selector::parse(&selector_str).map_err(|e| pyo3::exceptions::PyValueError::new_err(format!("Invalid CSS selector: {:?}", e)))?);
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

    // --- OPTIMIZATION: Pre-allocate result vectors ---
    let mut final_results = Vec::with_capacity(task_results.len());
    let mut latencies_ms = Vec::with_capacity(task_results.len());

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

/// The Python-facing function that bridges the async Rust world with the Python asyncio event loop.
///
/// This function is exposed to Python and uses `pyo3-asyncio` to convert the Rust `Future`
/// into a Python `Awaitable`.
#[pyfunction]
#[pyo3(text_signature = "(urls, selector, concurrency)")]
fn scrape_urls_concurrent(py: Python, urls: Vec<String>, selector: String, concurrency: usize) -> PyResult<&PyAny> {
    pyo3_asyncio::tokio::future_into_py(py, async move {
        scrape_all_urls(urls, selector, concurrency).await
    })
}

/// The Python module definition.
///
/// This function is called when the Python interpreter imports the module.
#[pymodule]
fn rust_scraper(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(scrape_urls_concurrent, m)?)?;
    Ok(())
}
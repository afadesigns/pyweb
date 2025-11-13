use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use scraper::{Html, Selector};
use rayon::prelude::*;
use ureq;

fn scrape_single_url(url: &str, selector_str: &str) -> Vec<String> {
    let body = match ureq::get(url).call() {
        Ok(resp) => match resp.into_string() {
            Ok(s) => s,
            Err(_) => return Vec::new(), // Return empty vec on string conversion error
        },
        Err(_) => return Vec::new(), // Return empty vec on request error
    };

    let fragment = Html::parse_document(&body);
    let sel = match Selector::parse(selector_str) {
        Ok(s) => s,
        Err(_) => return Vec::new(), // Return empty vec on selector parse error
    };

    fragment.select(&sel)
        .map(|element| element.text().collect::<String>())
        .collect()
}

#[pyfunction]
fn scrape_urls_concurrent(urls: Vec<String>, selector: String) -> PyResult<Vec<Vec<String>>> {
    let results: Vec<Vec<String>> = urls.par_iter()
        .map(|url| scrape_single_url(url, &selector))
        .collect();
    Ok(results)
}

#[pymodule]
fn rust_scraper(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(scrape_urls_concurrent, m)?)?;
    Ok(())
}

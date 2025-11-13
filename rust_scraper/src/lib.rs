use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use scraper::{Html, Selector};
use ureq;
use pyo3::exceptions::PyValueError;

#[pyfunction]
fn scrape(url: String, selector: String) -> PyResult<Vec<String>> {
    let body: String = ureq::get(&url)
        .call()
        .map_err(|e| PyValueError::new_err(e.to_string()))?
        .into_string()
        .map_err(|e| PyValueError::new_err(e.to_string()))?;

    let fragment = Html::parse_document(&body);
    let sel = Selector::parse(&selector).map_err(|e| PyValueError::new_err(format!("{:?}", e)))?;

    let mut elements = Vec::new();
    for element in fragment.select(&sel) {
        elements.push(element.text().collect::<String>());
    }

    Ok(elements)
}

#[pymodule]
fn rust_scraper(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(scrape, m)?)?;
    Ok(())
}
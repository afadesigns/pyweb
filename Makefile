.PHONY: setup build develop benchmark clean

# Variables
PYTHON = python3
VENV_DIR = .venv

setup:
	@echo ">>> Setting up Python virtual environment..."
	$(PYTHON) -m venv $(VENV_DIR)
	@echo ">>> Installing Python dependencies..."
	. $(VENV_DIR)/bin/activate && pip install -r requirements.txt
	@echo ">>> Setup complete. Activate the environment with: source $(VENV_DIR)/bin/activate"

build:
	@echo ">>> Building Rust core in release mode..."
	cd rust_scraper && maturin build --release

develop:
	@echo ">>> Installing Rust core in develop mode..."
	cd rust_scraper && maturin develop

benchmark:
	@echo ">>> Running performance benchmark..."
	. $(VENV_DIR)/bin/activate && python benchmarks/real_world_benchmark.py --pyweb-concurrency 175

clean:
	@echo ">>> Cleaning up build artifacts..."
	rm -rf rust_scraper/target
	rm -rf *.egg-info
	rm -rf __pycache__
	rm -f rust_scraper/*.so
	rm -f perf.data*
	@echo ">>> Done."

help:
	@echo "Available commands:"
	@echo "  setup      - Set up the Python virtual environment and install dependencies."
	@echo "  build      - Build the Rust extension in release mode."
	@echo "  develop    - Install the Rust extension in editable mode for development."
	@echo "  benchmark  - Run the definitive performance benchmark."
	@echo "  clean      - Remove all build artifacts and temporary files."

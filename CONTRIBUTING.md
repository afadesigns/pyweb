# Contributing to pyweb

First off, thank you for considering contributing to `pyweb`. It's people like you that make open source such a great community.

## Where do I go from here?

If you've noticed a bug or have a feature request, please [check the issues section](https://github.com/afadesigns/pyweb/issues) and see if it's already there. If not, please create a new one!

If you want to contribute code, please fork the repository and submit a pull request.

## Getting Started

1.  **Fork & Clone:** Fork the repository and clone it locally.
    ```bash
    git clone https://github.com/YOUR_USERNAME/pyweb.git
    cd pyweb
    ```

2.  **Set up the Environment:** Follow the instructions in the `Development` section of the `README.md`.

3.  **Make your changes:** Make your changes to the codebase.

4.  **Run the benchmarks:** Performance is the primary goal of this project. Please run the benchmark suite to ensure your changes have not introduced a regression.
    ```bash
    source .venv/bin/activate
    python benchmarks/real_world_benchmark.py
    ```

5.  **Submit a Pull Request:** Push your changes to your fork and submit a pull request to the `main` branch of the `afadesigns/pyweb` repository. Please provide a clear description of your changes and the results of the benchmark.

## Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms.

# Contributing to pyru

First off, thank you for considering contributing to `pyru`. It's people like you that make open source such a great community.

## Where do I go from here?

If you've noticed a bug or have a feature request, please [check the issues section](https://github.com/afadesigns/pyru/issues) and see if it's already there. If not, please create a new one!

If you want to contribute code, please fork the repository and submit a pull request.

## Getting Started

1.  **Fork & Clone:** Fork the repository and clone it locally.
    ```bash
    git clone https://github.com/YOUR_USERNAME/pyru.git
    cd pyru
    ```

## Development Environment Setup

This project uses a `Makefile` to streamline the development process. You will need Python 3.10+, the Rust toolchain (nightly), and `make`.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/afadesigns/pyru.git
    cd pyru
    ```

2.  **Set up the environment:** This will create a Python virtual environment and install all dependencies.
    ```bash
    make setup
    ```

3.  **Activate the environment:**
    ```bash
    source .venv/bin/activate
    ```

4.  **Build and install for development:** This installs the Rust core in an editable mode.
    ```bash
    make develop
    ```

## Commit Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification. This helps us maintain a clear commit history, automate changelog generation, and ensure consistent messaging. Please use the following types:

*   `feat`: New features
*   `fix`: Bug fixes
*   `docs`: Documentation changes
*   `ci`: CI/CD and workflow changes
*   `deps`: Dependency updates
*   `refactor`: Code refactoring (no behavior change)
*   `test`: Adding or correcting tests
*   `chore`: Routine maintenance

Example:
```
git commit -m "feat: add new scraper option"
```

3.  **Make your changes:** Make your changes to the codebase.

## Testing

Ensure your changes do not break existing functionality and ideally, add new tests for new features or bug fixes. The project uses `pytest` for unit tests and `zsh` scripts for integration tests.

*   **Run Unit Tests:**
    ```bash
    pytest
    ```

*   **Run Integration Tests:** (If applicable, specify path or command)
    ```bash
    # Example: zsh tests/integration_test.zsh
    ```

## Code Style and Linting

We enforce code quality and style using `ruff` for linting and formatting, and `mypy` for static type checking. Please ensure your code adheres to the established style.

*   **Run Linting and Formatting Checks:**
    ```bash
    ruff check .
    ruff format .
    ```

*   **Run Type Checking:**
    ```bash
    mypy .
    ```

4.  **Run the benchmarks:** Performance is the primary goal of this project. Please run the benchmark suite to ensure your changes have not introduced a regression.
    ```bash
    source .venv/bin/activate
    python benchmarks/real_world_benchmark.py
    ```

## Submit a Pull Request

1.  **Create a New Branch:** Create a branch from `main` with a descriptive name following the `type/description` convention (e.g., `feat/add-new-scraper-option`, `fix/resolve-parser-bug`).
    ```bash
    git checkout -b type/description
    ```

2.  **Push Changes:** Push your changes to your fork.

3.  **Open Pull Request:** Open a pull request against the `main` branch of the `afadesigns/pyru` repository. Please provide:
    *   A clear, concise description of your changes, referencing any relevant issues.
    *   The results of any benchmarks run (if applicable).
    *   Confirmation that tests pass and linting/type checks are clean.

We will review your pull request and provide feedback. Once approved, your changes will be merged.

## Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms.

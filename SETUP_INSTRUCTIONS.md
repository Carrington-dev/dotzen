# DotZen Development Setup Instructions

## Quick Fix for Current Error

The error you're seeing is because `pytest-cov` is not installed. Here are your options:

### Option 1: Install pytest-cov (Recommended)
```bash
pip install pytest-cov
```

Then run tests with coverage:
```bash
pytest --cov=dotzen --cov-report=term-missing --cov-report=html
```

### Option 2: Run tests without coverage
```bash
pytest
```

The `setup.cfg` has been updated to work without coverage by default.

---

## Full Development Setup

### 1. Install Development Dependencies

#### Using pip:
```bash
# Install all development dependencies
pip install -r requirements-dev.txt

# Or install the package in editable mode with dev extras
pip install -e ".[dev]"
```

#### Using the package extras:
```bash
# Basic + crypto
pip install -e ".[crypto]"

# Development tools
pip install -e ".[dev]"

# Everything
pip install -e ".[all]"
```

### 2. Running Tests

#### Basic test run:
```bash
pytest
```

#### With coverage:
```bash
pytest --cov=dotzen --cov-report=term-missing --cov-report=html
```

#### Parallel execution (faster):
```bash
pytest -n auto
```

#### Specific test file:
```bash
pytest tests/test_config_sources.py -v
```

#### Specific test class or function:
```bash
pytest tests/test_config_sources.py::TestEnvironmentSource -v
pytest tests/test_config_sources.py::TestEnvironmentSource::test_load_all_environment_variables -v
```

#### With markers:
```bash
# Run only unit tests
pytest -m unit

# Skip slow tests
pytest -m "not slow"

# Run only encryption tests
pytest -m encryption
```

### 3. Code Quality Tools

#### Format code with Black:
```bash
black dotzen tests
```

#### Sort imports with isort:
```bash
isort dotzen tests
```

#### Check code style with flake8:
```bash
flake8 dotzen tests
```

#### Type checking with mypy:
```bash
mypy dotzen
```

#### Run all quality checks:
```bash
black dotzen tests && isort dotzen tests && flake8 dotzen tests && mypy dotzen
```

### 4. Pre-commit Hooks (Optional)

Set up pre-commit hooks to automatically check code before commits:

```bash
# Install pre-commit
pip install pre-commit

# Install the git hooks
pre-commit install

# Run manually on all files
pre-commit run --all-files
```

### 5. Coverage Reports

After running tests with coverage, view the HTML report:

```bash
# Generate coverage
pytest --cov=dotzen --cov-report=html

# Open the report (Windows)
start htmlcov/index.html

# Open the report (macOS)
open htmlcov/index.html

# Open the report (Linux)
xdg-open htmlcov/index.html
```

---

## Project Structure

```
dotzen/
├── dotzen/
│   ├── __init__.py
│   ├── dotzen.py          # Core configuration module
│   ├── encryption.py      # Encryption support
│   ├── cli.py            # CLI interface
│   └── secrets/          # Cloud secrets (future)
│       ├── __init__.py
│       ├── base.py
│       ├── aws.py
│       ├── azure.py
│       └── gcp.py
├── tests/
│   ├── __init__.py
│   ├── test_config_sources.py
│   ├── test_config_builder.py
│   ├── test_config_factory.py
│   ├── test_type_casting.py
│   ├── test_edge_cases.py
│   └── test_encryption.py
├── setup.cfg
├── setup.py
├── pyproject.toml
├── requirements-dev.txt
├── README.md
└── LICENSE
```

---

## Common Issues and Solutions

### Issue: pytest-cov not found
**Solution:** Install pytest-cov
```bash
pip install pytest-cov
```

### Issue: Import errors when running tests
**Solution:** Install the package in editable mode
```bash
pip install -e .
```

### Issue: Tests can't find dotzen module
**Solution:** Make sure you're in the project root directory and have installed the package
```bash
cd /path/to/dotzen
pip install -e .
pytest
```

### Issue: Coverage not working
**Solution:** Ensure pytest-cov is installed and you're running from the project root
```bash
pip install pytest-cov
pytest --cov=dotzen
```

---

## CI/CD Integration

### GitHub Actions Example

Create `.github/workflows/tests.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.7', '3.8', '3.9', '3.10', '3.11', '3.12']
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"
    
    - name: Run tests with coverage
      run: |
        pytest --cov=dotzen --cov-report=xml --cov-report=term
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

---

## Quick Start for Contributors

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/dotzen.git
cd dotzen

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install in development mode
pip install -e ".[dev]"

# 4. Run tests
pytest

# 5. Make your changes and run tests again
pytest -v

# 6. Format and check code
black dotzen tests
flake8 dotzen tests

# 7. Commit and push
git add .
git commit -m "Your changes"
git push
```

---

## Useful Commands Cheat Sheet

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_encryption.py

# Run tests matching pattern
pytest -k "test_encrypt"

# Run with coverage
pytest --cov=dotzen --cov-report=html

# Run in parallel (faster)
pytest -n auto

# Stop on first failure
pytest -x

# Show print statements
pytest -s

# Run last failed tests
pytest --lf

# Run tests that failed last time, then all others
pytest --ff
```
# Contributing to DotZen 🧘

First off, thank you for considering contributing to DotZen! It's people like you that make DotZen such a great tool for the Python community.

## 📜 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Your First Code Contribution](#your-first-code-contribution)
  - [Pull Requests](#pull-requests)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Style Guidelines](#style-guidelines)
  - [Git Commit Messages](#git-commit-messages)
  - [Python Style Guide](#python-style-guide)
  - [Documentation Style Guide](#documentation-style-guide)
- [Testing Guidelines](#testing-guidelines)
- [Community](#community)

---

## Code of Conduct

This project and everyone participating in it is governed by our commitment to providing a welcoming and inclusive environment. By participating, you are expected to uphold this code. Please be respectful and constructive in all interactions.

### Our Standards

**Examples of behavior that contributes to a positive environment:**

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Examples of unacceptable behavior:**

- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without explicit permission
- Other conduct which could reasonably be considered inappropriate in a professional setting

---

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report for DotZen. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

**Before Submitting A Bug Report:**

- Check the [documentation](https://dotzen.readthedocs.io) to ensure you're using the library correctly
- Check the [existing issues](https://github.com/carrington-dev/dotzen/issues) to see if the problem has already been reported
- Try to reproduce the issue with the latest version of DotZen

**How Do I Submit A Good Bug Report?**

Bugs are tracked as [GitHub issues](https://github.com/carrington-dev/dotzen/issues). Create an issue and provide the following information:

- **Use a clear and descriptive title** for the issue to identify the problem
- **Describe the exact steps to reproduce the problem** in as much detail as possible
- **Provide specific examples** to demonstrate the steps
- **Describe the behavior you observed** after following the steps
- **Explain which behavior you expected to see instead** and why
- **Include code snippets** and error messages
- **Include your environment details:**
  - DotZen version
  - Python version
  - Operating system
  - Any relevant cloud provider SDK versions (if using cloud secrets)

**Bug Report Template:**

```markdown
**Description:**
A clear and concise description of the bug.

**To Reproduce:**
Steps to reproduce the behavior:
1. Create a config with '...'
2. Call method '...'
3. See error

**Expected Behavior:**
A clear description of what you expected to happen.

**Actual Behavior:**
What actually happened.

**Code Sample:**
```python
from dotzen import ConfigBuilder

config = ConfigBuilder()...
# Code that demonstrates the issue
```

**Environment:**
- DotZen version: [e.g., 1.1.0]
- Python version: [e.g., 3.11.5]
- OS: [e.g., Ubuntu 22.04]
- Cloud SDK versions (if applicable): [e.g., boto3 1.28.0]

**Additional Context:**
Any other context about the problem.
```

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for DotZen, including completely new features and minor improvements to existing functionality.

**Before Submitting An Enhancement Suggestion:**

- Check the [documentation](https://dotzen.readthedocs.io) to see if the feature already exists
- Check the [existing issues](https://github.com/carrington-dev/dotzen/issues) and [discussions](https://github.com/carrington-dev/dotzen/discussions) to see if the enhancement has already been suggested

**How Do I Submit A Good Enhancement Suggestion?**

Enhancement suggestions are tracked as [GitHub issues](https://github.com/carrington-dev/dotzen/issues) or [discussions](https://github.com/carrington-dev/dotzen/discussions). Create an issue/discussion and provide the following information:

- **Use a clear and descriptive title** for the issue/discussion
- **Provide a step-by-step description of the suggested enhancement** with as much detail as possible
- **Provide specific examples** to demonstrate the steps or point out where the enhancement would be useful
- **Describe the current behavior** and **explain which behavior you expected to see instead**
- **Explain why this enhancement would be useful** to most DotZen users

**Enhancement Suggestion Template:**

```markdown
**Feature Description:**
A clear and concise description of the feature.

**Problem It Solves:**
Explain the problem this feature would solve.

**Proposed Solution:**
Describe how you envision this feature working.

**Alternative Solutions:**
Describe any alternative solutions or features you've considered.

**Code Example:**
```python
# Show how the feature would be used
config = ConfigBuilder()
    .add_custom_feature(...)
    .build()
```

**Additional Context:**
Any other context, screenshots, or examples.
```

### Your First Code Contribution

Unsure where to begin contributing? You can start by looking through these beginner-friendly issues:

- **Good First Issue** - Issues that should only require a few lines of code
- **Help Wanted** - Issues that may be more involved but are good entry points

**Working on your first Pull Request?** You can learn how from this free series:
[How to Contribute to an Open Source Project on GitHub](https://egghead.io/courses/how-to-contribute-to-an-open-source-project-on-github)

### Pull Requests

The process described here has several goals:

- Maintain DotZen's quality
- Fix problems that are important to users
- Engage the community in working toward the best possible DotZen
- Enable a sustainable system for DotZen's maintainers to review contributions

**Please follow these steps to have your contribution considered by the maintainers:**

1. Follow all instructions in the [pull request template](.github/PULL_REQUEST_TEMPLATE)
2. Follow the [style guidelines](#style-guidelines)
3. After you submit your pull request, verify that all [status checks](https://help.github.com/articles/about-status-checks/) are passing

**What if the status checks are failing?**

If a status check is failing, it's your responsibility to fix it. If you believe that the failure is unrelated to your change, please leave a comment explaining why you believe it's unrelated.

---

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- pip and virtualenv (or your preferred virtual environment tool)

### Setting Up Your Development Environment

1. **Fork the repository** on GitHub

2. **Clone your fork locally:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/dotzen.git
   cd dotzen
   ```

3. **Add the upstream repository:**
   ```bash
   git remote add upstream https://github.com/carrington-dev/dotzen.git
   ```

4. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

5. **Install development dependencies:**
   ```bash
   pip install -e ".[dev,test,all]"
   ```

6. **Install pre-commit hooks:**
   ```bash
   pre-commit install
   ```

7. **Verify your setup:**
   ```bash
   pytest
   ```

### Project Structure

```
dotzen/
├── dotzen/              # Main package code
│   ├── __init__.py
│   ├── config.py        # Core Config class
│   ├── builder.py       # ConfigBuilder pattern
│   ├── sources/         # Configuration sources
│   │   ├── base.py
│   │   ├── environment.py
│   │   ├── dotenv.py
│   │   ├── json_source.py
│   │   └── ...
│   ├── validators/      # Validation framework
│   └── exceptions.py    # Custom exceptions
├── tests/               # Test suite
│   ├── test_config.py
│   ├── test_builder.py
│   ├── test_sources/
│   └── ...
├── docs/                # Documentation
├── examples/            # Usage examples
├── .github/             # GitHub workflows and templates
├── pyproject.toml       # Project metadata and dependencies
├── setup.py             # Setup configuration
├── pytest.ini           # Pytest configuration
└── README.md            # Project README
```

---

## Development Workflow

### Creating a Branch

Always create a new branch for your work:

```bash
# Update your local main branch
git checkout main
git pull upstream main

# Create a new feature branch
git checkout -b feature/your-feature-name

# Or for a bug fix
git checkout -b fix/bug-description
```

**Branch naming conventions:**

- `feature/feature-name` - For new features
- `fix/bug-description` - For bug fixes
- `docs/update-description` - For documentation updates
- `refactor/description` - For code refactoring
- `test/test-description` - For test improvements

### Making Changes

1. **Make your changes** following our [style guidelines](#style-guidelines)

2. **Write or update tests** for your changes

3. **Run the test suite:**
   ```bash
   pytest
   ```

4. **Run code quality checks:**
   ```bash
   # Format code with black
   black dotzen tests
   
   # Run linting with ruff
   ruff check dotzen tests
   
   # Type checking with mypy
   mypy dotzen
   ```

5. **Check test coverage:**
   ```bash
   pytest --cov=dotzen --cov-report=html
   # Open htmlcov/index.html in your browser
   ```

### Committing Your Changes

1. **Stage your changes:**
   ```bash
   git add .
   ```

2. **Commit with a descriptive message:**
   ```bash
   git commit -m "Add feature: description"
   ```

3. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

### Submitting a Pull Request

1. **Go to the [DotZen repository](https://github.com/carrington-dev/dotzen)**

2. **Click "New Pull Request"**

3. **Select your fork and branch**

4. **Fill out the pull request template**

5. **Submit the pull request**

6. **Respond to review feedback**

---

## Style Guidelines

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line
- Consider starting the commit message with an applicable emoji:
  - ✨ `:sparkles:` - New feature
  - 🐛 `:bug:` - Bug fix
  - 📝 `:memo:` - Documentation
  - 🎨 `:art:` - Code structure/format improvement
  - ⚡ `:zap:` - Performance improvement
  - ✅ `:white_check_mark:` - Adding tests
  - 🔧 `:wrench:` - Configuration files
  - 🔥 `:fire:` - Removing code/files
  - ♻️ `:recycle:` - Refactoring

**Examples:**

```
✨ Add support for Azure Key Vault integration

🐛 Fix type casting error in get_list method

Resolves #123

📝 Update installation instructions in README

Added section on cloud provider extras
```

### Python Style Guide

DotZen follows the [PEP 8](https://pep8.org/) style guide with some specific conventions:

#### Code Formatting

- **Use Black** for automatic code formatting (120 character line length)
- **Use Ruff** for linting and additional code quality checks
- **Use mypy** for type checking

#### Type Hints

Always use type hints for function signatures:

```python
from typing import Dict, List, Optional, Any

def get_value(
    key: str,
    default: Optional[Any] = None,
    cast: Optional[type] = None
) -> Any:
    """Get a configuration value with optional casting."""
    pass
```

#### Docstrings

Use Google-style docstrings:

```python
def add_environment(self, prefix: str = "") -> "ConfigBuilder":
    """Add environment variables as a configuration source.
    
    Args:
        prefix: Optional prefix to filter environment variables.
                Only variables starting with this prefix will be loaded.
    
    Returns:
        The ConfigBuilder instance for method chaining.
    
    Example:
        >>> config = (ConfigBuilder()
        ...     .add_environment('APP_')
        ...     .build())
    """
    pass
```

#### Imports

Organize imports in the following order:

1. Standard library imports
2. Third-party imports
3. Local application imports

Use absolute imports when possible:

```python
# Standard library
import os
from typing import Dict, List

# Third-party
import pytest

# Local
from dotzen.config import Config
from dotzen.sources.base import ConfigSource
```

#### Naming Conventions

- **Classes**: `PascalCase` (e.g., `ConfigBuilder`, `EnvironmentSource`)
- **Functions/Methods**: `snake_case` (e.g., `add_environment`, `get_bool`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `DEFAULT_ENCODING`, `MAX_RETRIES`)
- **Private methods/attributes**: `_leading_underscore` (e.g., `_load_data`)

### Documentation Style Guide

- Write clear, concise documentation
- Include code examples for all public APIs
- Update relevant documentation when changing functionality
- Use proper Markdown formatting
- Include links to related documentation

---

## Testing Guidelines

### Writing Tests

- **Write tests for all new features and bug fixes**
- **Follow the Arrange-Act-Assert pattern:**
  ```python
  def test_get_bool_conversion():
      # Arrange
      config = ConfigBuilder().add_environment().build()
      os.environ['TEST_BOOL'] = 'true'
      
      # Act
      result = config.get_bool('TEST_BOOL')
      
      # Assert
      assert result is True
      assert isinstance(result, bool)
  ```

- **Use descriptive test names:**
  ```python
  def test_get_bool_returns_true_for_truthy_strings():
      pass
  
  def test_config_builder_raises_error_when_required_value_missing():
      pass
  ```

- **Test edge cases and error conditions:**
  ```python
  def test_get_int_raises_validation_error_for_invalid_input():
      config = ConfigBuilder().add_environment().build()
      os.environ['INVALID_INT'] = 'not-a-number'
      
      with pytest.raises(ValidationError):
          config.get_int('INVALID_INT')
  ```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=dotzen --cov-report=html

# Run specific test file
pytest tests/test_config.py

# Run specific test
pytest tests/test_config.py::test_get_bool_conversion

# Run tests matching pattern
pytest -k "test_builder"

# Run tests with verbose output
pytest -v

# Run tests and stop on first failure
pytest -x
```

### Test Categories

Tests are organized into categories using pytest markers:

```python
@pytest.mark.unit
def test_config_get_value():
    """Unit tests for core functionality"""
    pass

@pytest.mark.integration
def test_aws_secrets_integration():
    """Integration tests with external services"""
    pass

@pytest.mark.slow
def test_large_config_file():
    """Tests that take longer to run"""
    pass
```

Run specific categories:

```bash
# Run only unit tests
pytest -m unit

# Run all except integration tests
pytest -m "not integration"

# Run fast tests only
pytest -m "not slow"
```

### Coverage Requirements

- Maintain **minimum 80% code coverage** for all new code
- Aim for **90%+ coverage** on core functionality
- Focus on testing critical paths and edge cases
- Don't write tests just to increase coverage numbers

---

## Community

### Getting Help

- 📚 **Documentation**: [dotzen.readthedocs.io](https://dotzen.readthedocs.io)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/carrington-dev/dotzen/discussions)
- 🐛 **Issues**: [GitHub Issues](https://github.com/carrington-dev/dotzen/issues)
- 📧 **Email**: carrington.muleya@outlook.com

### Stay Updated

- ⭐ **Star** the repository to receive updates
- 👁️ **Watch** the repository for notifications
- 🔔 **Subscribe** to release notifications

---

## Recognition

Contributors will be recognized in the following ways:

- Listed in the project's [contributors](https://github.com/carrington-dev/dotzen/graphs/contributors) page
- Mentioned in release notes for significant contributions
- Added to the README acknowledgments section for major contributions

---

## Questions?

Don't hesitate to ask questions! You can:

- Open a [discussion](https://github.com/carrington-dev/dotzen/discussions) for general questions
- Create an [issue](https://github.com/carrington-dev/dotzen/issues) for specific problems
- Reach out via email at carrington.muleya@outlook.com

---

## Thank You! 🙏

Your contributions to open source, large or small, make projects like DotZen possible. Thank you for taking the time to contribute!

**Happy coding, and may your configurations always be zen! 🧘✨**
"""
DotZen - Find your configuration zen.
Peaceful, type-safe Python configuration that just works.
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read version from package
def get_version():
    """Read version from __version__.py"""
    version_file = this_directory / "dotzen" / "__version__.py"
    version_dict = {}
    with open(version_file) as f:
        exec(f.read(), version_dict)
    return version_dict['__version__']

setup(
    name="dotzen",
    version=get_version(),
    author="Carrington Muleya",
    author_email="carrington.muleya@outlook.com",
    description="Peaceful, type-safe Python configuration with strict separation from code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/carrington-dev/dotzen",
    project_urls={
        "Bug Tracker": "https://github.com/carrington-dev/dotzen/issues",
        "Documentation": "https://dotzen.readthedocs.io",
        "Source Code": "https://github.com/carrington-dev/dotzen",
        "Changelog": "https://github.com/carrington-dev/dotzen/blob/main/CHANGELOG.md",
    },
    packages=find_packages(exclude=["tests", "tests.*", "examples", "docs"]),
    classifiers=[
        # Development Status
        "Development Status :: 4 - Beta",
        
        # Intended Audience
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        
        # Topic
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
        
        # License
        "License :: OSI Approved :: MIT License",
        
        # Python Versions
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        
        # Other
        "Operating System :: OS Independent",
        "Typing :: Typed",
        "Natural Language :: English",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0",
        "typing-extensions>=4.0.0; python_version < '3.10'",
    ],
    extras_require={
        # Cloud Secret Managers
        "aws": [
            "boto3>=1.26.0",
            "botocore>=1.29.0",
        ],
        "gcp": [
            "google-cloud-secret-manager>=2.16.0",
        ],
        "azure": [
            "azure-keyvault-secrets>=4.7.0",
            "azure-identity>=1.12.0",
        ],
        "vault": [
            "hvac>=1.2.0",  # HashiCorp Vault
        ],
        
        # Multiple format support
        "yaml": [
            "PyYAML>=6.0",
        ],
        "toml": [
            "tomli>=2.0.0; python_version < '3.11'",
        ],
        "json5": [
            "json5>=0.9.0",
        ],
        
        # All cloud providers
        "cloud": [
            "boto3>=1.26.0",
            "google-cloud-secret-manager>=2.16.0",
            "azure-keyvault-secrets>=4.7.0",
            "azure-identity>=1.12.0",
            "hvac>=1.2.0",
        ],
        
        # All format support
        "formats": [
            "PyYAML>=6.0",
            "tomli>=2.0.0; python_version < '3.11'",
            "json5>=0.9.0",
        ],
        
        # Development dependencies
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-mock>=3.10.0",
            "black>=23.0.0",
            "ruff>=0.1.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
            "tox>=4.0.0",
        ],
        
        # Documentation
        "docs": [
            "sphinx>=6.0.0",
            "sphinx-rtd-theme>=1.2.0",
            "sphinx-autodoc-typehints>=1.22.0",
            "myst-parser>=1.0.0",
        ],
        
        # Testing with cloud providers
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-mock>=3.10.0",
            "moto[secretsmanager]>=4.0.0",  # Mock AWS
            "responses>=0.23.0",
        ],
        
        # Everything
        "all": [
            # Cloud providers
            "boto3>=1.26.0",
            "google-cloud-secret-manager>=2.16.0",
            "azure-keyvault-secrets>=4.7.0",
            "azure-identity>=1.12.0",
            "hvac>=1.2.0",
            # Formats
            "PyYAML>=6.0",
            "tomli>=2.0.0; python_version < '3.11'",
            "json5>=0.9.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "dotzen=dotzen.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "dotzen": [
            "py.typed",  # PEP 561 marker for type information
            "templates/*.template",
        ],
    },
    zip_safe=False,
    keywords=[
        "configuration",
        "config",
        "settings",
        "environment",
        "env",
        "dotenv",
        "secrets",
        "cloud",
        "aws",
        "gcp",
        "azure",
        "type-safe",
        "validation",
        "pydantic",
        "secrets-manager",
        "key-vault",
    ],
)

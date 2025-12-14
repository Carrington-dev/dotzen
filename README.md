<div align="center">

# 🧘 DotZen

**Peaceful, type-safe Python configuration that just works.**

[![PyPI version](https://badge.fury.io/py/dotzen.svg)](https://badge.fury.io/py/dotzen)
[![Python Support](https://img.shields.io/pypi/pyversions/dotzen.svg)](https://pypi.org/project/dotzen/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/carrington-dev/dotzen/workflows/Tests/badge.svg)](https://github.com/carrington-dev/dotzen/actions)
[![codecov](https://codecov.io/gh/carrington-dev/dotzen/branch/main/graph/badge.svg)](https://codecov.io/gh/carrington-dev/dotzen)
[![Documentation Status](https://readthedocs.org/projects/dotzen/badge/?version=latest)](https://dotzen.readthedocs.io/en/latest/?badge=latest)
[![Downloads](https://pepy.tech/badge/dotzen/month)](https://pepy.tech/project/dotzen)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[Documentation](https://dotzen.readthedocs.io) | [PyPI Package](https://pypi.org/project/dotzen/) | [GitHub](https://github.com/carrington-dev/dotzen) | [Changelog](CHANGELOG.md)

</div>

---

## 🌟 Overview

DotZen brings **zen** to Python configuration management. Load settings from environment variables, `.env` files, JSON, YAML, or cloud secret managers with automatic type casting, validation, and a beautiful fluent API.

**No more config chaos. Just pure zen.** 🧘‍♂️✨

### ✨ Key Highlights

```python
from dotzen import config

# Simple, elegant, type-safe
DEBUG = config('DEBUG', cast=bool, default=False)
PORT = config('PORT', cast=int, default=8000)
DATABASE_URL = config('DATABASE_URL')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=list)
```

### Why Choose DotZen?

| Traditional Config | 😫 | DotZen | ✨ |
|-------------------|-----|---------|-----|
| Scattered sources | Multiple libraries needed | **Unified API** | One interface for all sources |
| String soup | Manual type conversion everywhere | **Type Safety** | Automatic casting & validation |
| Runtime failures | Errors only in production | **Early Validation** | Catch issues at startup |
| Copy-paste code | Boilerplate in every project | **Design Patterns** | Elegant, reusable architecture |
| Hardcoded secrets | Security nightmares | **Cloud-Native** | First-class secrets support |

---

## 🚀 Quick Start

### Installation

```bash
# Core library (zero dependencies)
pip install dotzen

# With cloud provider support
pip install dotzen[aws]        # AWS Secrets Manager
pip install dotzen[gcp]        # Google Cloud Secret Manager
pip install dotzen[azure]      # Azure Key Vault
pip install dotzen[cloud]      # All cloud providers

# Everything included
pip install dotzen[all]
```

### Basic Usage

```python
from dotzen import config

# Get configuration values with automatic type casting
API_KEY = config('API_KEY')
DEBUG = config('DEBUG', cast=bool, default=False)
MAX_CONNECTIONS = config('MAX_CONNECTIONS', cast=int, default=100)
ALLOWED_ORIGINS = config('ALLOWED_ORIGINS', cast=list)
```

### Advanced Usage with Builder Pattern

```python
from dotzen import ConfigBuilder

# Build a configuration with multiple sources
config = (ConfigBuilder()
    .add_environment('APP_')        # Env vars with prefix
    .add_dotenv('.env')             # .env file
    .add_json('config.json')        # JSON config
    .add_secrets('/run/secrets')    # Docker secrets
    .build())

# Type-safe access with convenience methods
debug = config.get_bool('DEBUG', default=False)
port = config.get_int('PORT', default=8000)
timeout = config.get_float('TIMEOUT', default=30.0)
hosts = config.get_list('ALLOWED_HOSTS')
```

---

## 🎯 Features

### 🔄 Multi-Source Configuration

DotZen implements a **Chain of Responsibility** pattern, checking sources in priority order:

```python
config = (ConfigBuilder()
    .add_environment()           # 1️⃣ Highest priority
    .add_dotenv('.env')          # 2️⃣
    .add_json('config.json')     # 3️⃣
    .add_aws_secrets('prod')     # 4️⃣
    .build())                    # 5️⃣ Default values (lowest priority)
```

### 🛡️ Type Safety & Automatic Casting

```python
# Automatic type conversion with validation
DEBUG = config.get_bool('DEBUG')           # str → bool
PORT = config.get_int('PORT')              # str → int
RATE_LIMIT = config.get_float('RATE')     # str → float
SERVERS = config.get_list('SERVERS')       # str → list

# Boolean casting supports multiple formats
# True:  "true", "yes", "1", "on", "t", "y"
# False: "false", "no", "0", "off", "f", "n"
```

### ✅ Built-in Validation

```python
from dotzen import ConfigBuilder
from dotzen.validators import URLValidator, RangeValidator, RegexValidator

config = (ConfigBuilder()
    .add_environment()
    .with_validator(URLValidator('DATABASE_URL'))
    .with_validator(RangeValidator('PORT', 1024, 65535))
    .with_validator(RegexValidator('API_KEY', r'^[A-Za-z0-9]{32}$'))
    .build())

# Configuration is validated at build time
# Errors are caught before your app starts! 🎉
```

### 🌐 Cloud Secrets Support

```python
# AWS Secrets Manager
config = (ConfigBuilder()
    .add_environment()
    .add_aws_secrets('prod/myapp', region='us-east-1')
    .build())

# Google Cloud Secret Manager
config = (ConfigBuilder()
    .add_environment()
    .add_gcp_secrets('projects/my-project/secrets')
    .build())

# Azure Key Vault
config = (ConfigBuilder()
    .add_environment()
    .add_azure_keyvault('https://myvault.vault.azure.net')
    .build())

# HashiCorp Vault
config = (ConfigBuilder()
    .add_environment()
    .add_vault_secrets('secret/myapp', url='https://vault.example.com')
    .build())
```

### 🎨 Fluent API Design

DotZen uses the **Builder Pattern** for an intuitive, chainable API:

```python
config = (ConfigBuilder()
    .add_environment('MYAPP_')
    .add_dotenv('.env')
    .add_dotenv('.env.local', override=True)
    .add_json('config.json')
    .add_yaml('settings.yaml')
    .with_validator(URLValidator('DATABASE_URL'))
    .with_type('MAX_WORKERS', int)
    .build())
```

### 🏭 Auto-Detection Factory

Let DotZen automatically detect your configuration files:

```python
from dotzen import ConfigFactory

# Automatically finds and loads:
# - .env
# - config.json
# - settings.json
config = ConfigFactory.auto_config()
```

---

## 📚 Real-World Examples

### Django Settings

```python
# settings.py
from dotzen import config

# Core settings
DEBUG = config('DEBUG', cast=bool, default=False)
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=list, default=[])

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', cast=int, default=5432),
    }
}

# Email configuration
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', cast=int, default=587)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool, default=True)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

# Redis cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': config('REDIS_URL', default='redis://127.0.0.1:6379/1'),
    }
}
```

### FastAPI Application

```python
from fastapi import FastAPI, Depends
from dotzen import ConfigBuilder

# Build configuration at startup
config = (ConfigBuilder()
    .add_environment()
    .add_dotenv()
    .add_json('config.json')
    .build())

app = FastAPI(
    title=config('APP_NAME', default='My API'),
    debug=config.get_bool('DEBUG', default=False),
    version=config('VERSION', default='1.0.0'),
)

# Dependency injection
def get_database_url():
    return config('DATABASE_URL')

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": config('ENVIRONMENT', default='development'),
        "version": config('VERSION', default='1.0.0'),
    }

@app.get("/config")
async def get_config_info():
    return {
        "debug_mode": config.get_bool('DEBUG', False),
        "max_connections": config.get_int('MAX_CONNECTIONS', 100),
        "timeout": config.get_float('TIMEOUT', 30.0),
    }
```

### Flask Application

```python
from flask import Flask
from dotzen import config

app = Flask(__name__)

# Configure Flask from DotZen
app.config['DEBUG'] = config('DEBUG', cast=bool, default=False)
app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Custom settings
app.config['MAX_CONTENT_LENGTH'] = config('MAX_UPLOAD_SIZE', cast=int, default=16 * 1024 * 1024)
app.config['UPLOAD_FOLDER'] = config('UPLOAD_FOLDER', default='uploads')

@app.route('/config')
def show_config():
    return {
        'debug': app.config['DEBUG'],
        'environment': config('ENVIRONMENT', default='development'),
    }
```

### Microservices with Docker Secrets

```python
# docker-compose.yml provides secrets in /run/secrets/
from dotzen import ConfigBuilder

config = (ConfigBuilder()
    .add_environment()
    .add_secrets('/run/secrets')  # Docker secrets
    .add_dotenv('.env')
    .build())

# Access secrets seamlessly
DB_PASSWORD = config('db_password')
API_KEY = config('api_key')
JWT_SECRET = config('jwt_secret')

# Regular config
SERVICE_NAME = config('SERVICE_NAME', default='my-service')
PORT = config.get_int('PORT', default=8000)
```

### Multi-Environment Configuration

```python
import os
from dotzen import ConfigBuilder

# Determine environment
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# Load environment-specific configuration
config = (ConfigBuilder()
    .add_environment()
    .add_dotenv(f'.env.{ENVIRONMENT}')      # .env.development, .env.production
    .add_json(f'config.{ENVIRONMENT}.json')
    .add_dotenv('.env.local', override=True)  # Local overrides
    .build())

# Configuration adapts to environment automatically
DEBUG = config.get_bool('DEBUG')
DATABASE_URL = config('DATABASE_URL')
LOG_LEVEL = config('LOG_LEVEL', default='INFO')
```

### Pydantic Integration

```python
from pydantic import BaseModel, Field
from dotzen import config

class DatabaseSettings(BaseModel):
    host: str = Field(default_factory=lambda: config('DB_HOST', default='localhost'))
    port: int = Field(default_factory=lambda: config('DB_PORT', cast=int, default=5432))
    user: str = Field(default_factory=lambda: config('DB_USER'))
    password: str = Field(default_factory=lambda: config('DB_PASSWORD'))
    database: str = Field(default_factory=lambda: config('DB_NAME'))

class AppSettings(BaseModel):
    debug: bool = Field(default_factory=lambda: config('DEBUG', cast=bool, default=False))
    secret_key: str = Field(default_factory=lambda: config('SECRET_KEY'))
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    allowed_hosts: list = Field(default_factory=lambda: config('ALLOWED_HOSTS', cast=list, default=[]))

# Create settings instance
settings = AppSettings()
```

---

## 🏗️ Architecture & Design Patterns

DotZen is built on proven **Gang of Four** design patterns:

### Design Patterns Used

| Pattern | Purpose | Implementation |
|---------|---------|----------------|
| **Strategy** | Pluggable config sources | `ConfigSource` abstract base class |
| **Chain of Responsibility** | Priority-based resolution | `ConfigChain` tries sources in order |
| **Builder** | Fluent construction | `ConfigBuilder` for chainable API |
| **Factory** | Auto-detection | `ConfigFactory.auto_config()` |
| **Singleton** | Global instance | `ConfigSingleton` for app-wide access |
| **Facade** | Simple interface | `Config` class hides complexity |
| **Null Object** | Graceful defaults | `NullSource` for missing configs |
| **Sentinel** | Undefined values | `UNDEFINED` marker object |

### Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│                   ConfigBuilder                      │
│              (Builder Pattern)                       │
└───────────────────┬─────────────────────────────────┘
                    │ builds
                    ▼
┌─────────────────────────────────────────────────────┐
│                     Config                           │
│                (Facade Pattern)                      │
└───────────────────┬─────────────────────────────────┘
                    │ uses
                    ▼
┌─────────────────────────────────────────────────────┐
│                  ConfigChain                         │
│        (Chain of Responsibility Pattern)             │
└───────────────────┬─────────────────────────────────┘
                    │ coordinates
                    ▼
┌─────────────────────────────────────────────────────┐
│              ConfigSource (Strategy)                 │
│  ┌──────────────────────────────────────────────┐  │
│  │ EnvironmentSource │ DotEnvSource │ JsonSource│  │
│  │ YamlSource │ SecretSource │ AwsSecretsSource │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## 🆚 Comparison with Alternatives

### Feature Comparison Matrix

| Feature | DotZen | python-decouple | pydantic-settings | dynaconf | python-dotenv |
|---------|:------:|:---------------:|:-----------------:|:--------:|:-------------:|
| **Type Safety** | ✅ Full | ⚠️ Basic | ✅ Full | ✅ Full | ❌ None |
| **Cloud Secrets** | ✅ Native | ❌ No | ⚠️ Limited | ✅ Yes | ❌ No |
| **Fluent API** | ✅ Yes | ❌ No | ❌ No | ⚠️ Limited | ❌ No |
| **Validation** | ✅ Built-in | ⚠️ Basic | ✅ Pydantic | ✅ Yes | ❌ No |
| **Multi-Source** | ✅ Yes | ⚠️ Limited | ⚠️ Limited | ✅ Yes | ❌ Env only |
| **Zero Core Deps** | ✅ Yes | ✅ Yes | ❌ No | ❌ No | ✅ Yes |
| **Design Patterns** | ✅ 8 patterns | ❌ None | ⚠️ Some | ⚠️ Some | ❌ None |
| **Docker Secrets** | ✅ Native | ❌ No | ❌ No | ❌ No | ❌ No |
| **Auto-Detection** | ✅ Yes | ❌ No | ⚠️ Limited | ✅ Yes | ❌ No |
| **Custom Sources** | ✅ Easy | ❌ No | ⚠️ Complex | ⚠️ Complex | ❌ No |

### When to Use DotZen

**Perfect for:**
- 🚀 Modern cloud-native applications
- 🏢 Microservices architectures
- 📦 12-factor app compliance
- 🔐 Applications requiring cloud secrets
- 👥 Teams valuing clean, maintainable code
- 🎯 Projects needing validated configuration

**Consider alternatives if:**
- You only need basic `.env` file parsing → `python-dotenv`
- You're heavily invested in Pydantic → `pydantic-settings`
- You need legacy Python 2.7 support → `python-decouple`

---

## 📖 Documentation

### Core Concepts

#### Configuration Sources

```python
from dotzen import ConfigBuilder

# Available sources
builder = ConfigBuilder()
builder.add_environment()              # Environment variables
builder.add_environment('APP_')        # With prefix
builder.add_dotenv('.env')             # .env file
builder.add_json('config.json')        # JSON file
builder.add_yaml('config.yaml')        # YAML file (requires dotzen[yaml])
builder.add_toml('config.toml')        # TOML file (requires dotzen[toml])
builder.add_secrets('/run/secrets')    # Docker secrets
builder.add_aws_secrets('prod/myapp')  # AWS Secrets Manager
builder.add_gcp_secrets('projects/x')  # GCP Secret Manager
builder.add_azure_keyvault('url')      # Azure Key Vault
builder.add_vault_secrets('path')      # HashiCorp Vault
```

#### Type Casting

```python
# Automatic casting
value = config.get('KEY', cast=int)
value = config.get('KEY', cast=bool)
value = config.get('KEY', cast=float)
value = config.get('KEY', cast=list)

# Convenience methods
value = config.get_int('KEY', default=0)
value = config.get_bool('KEY', default=False)
value = config.get_float('KEY', default=0.0)
value = config.get_list('KEY', default=[])

# Custom casting
def parse_json(value):
    import json
    return json.loads(value)

value = config.get('JSON_DATA', cast=parse_json)
```

#### Error Handling

```python
from dotzen import UndefinedValueError, ValidationError, ConfigError

try:
    api_key = config('API_KEY')
except UndefinedValueError:
    print("API_KEY not found in configuration")

try:
    port = config.get_int('PORT')
except ValidationError as e:
    print(f"Invalid PORT value: {e}")

# Or use defaults
api_key = config('API_KEY', default='dev-key')
port = config.get_int('PORT', default=8000)
```

### Advanced Usage

#### Custom Configuration Sources

```python
from dotzen import ConfigSource

class RedisSource(ConfigSource):
    """Load configuration from Redis"""
    
    def __init__(self, redis_client, prefix='config:'):
        self.redis = redis_client
        self.prefix = prefix
    
    def load(self) -> Dict[str, str]:
        keys = self.redis.keys(f'{self.prefix}*')
        data = {}
        for key in keys:
            clean_key = key.decode().replace(self.prefix, '')
            data[clean_key] = self.redis.get(key).decode()
        return data
    
    def exists(self) -> bool:
        return self.redis.ping()

# Use custom source
import redis
redis_client = redis.Redis(host='localhost', port=6379)

config = (ConfigBuilder()
    .add_custom_source(RedisSource(redis_client))
    .build())
```

#### Custom Validators

```python
from dotzen import ConfigBuilder, ValidationError

def email_validator(key: str, value: str):
    """Validate email format"""
    if '@' not in value:
        raise ValidationError(f"{key} must be a valid email")

def port_validator(key: str, value: int):
    """Validate port number"""
    if not (1024 <= value <= 65535):
        raise ValidationError(f"{key} must be between 1024 and 65535")

config = (ConfigBuilder()
    .add_environment()
    .with_validator(email_validator)
    .with_type('PORT', int)
    .with_validator(port_validator)
    .build())
```

#### Testing Configuration

```python
import pytest
from dotzen import ConfigBuilder, ConfigSingleton

def test_config():
    """Test configuration loading"""
    # Reset singleton for testing
    ConfigSingleton.reset()
    
    # Create test config
    config = (ConfigBuilder()
        .add_environment()
        .build())
    
    # Test values
    assert config.get_bool('DEBUG', False) == False
    assert config.get_int('PORT', 8000) == 8000

@pytest.fixture
def test_config():
    """Fixture providing test configuration"""
    ConfigSingleton.reset()
    return (ConfigBuilder()
        .add_dotenv('.env.test')
        .build())
```

---

## 🔧 Installation Extras

### Available Extras

```bash
# Cloud providers
pip install dotzen[aws]        # AWS Secrets Manager (boto3)
pip install dotzen[gcp]        # Google Cloud Secret Manager
pip install dotzen[azure]      # Azure Key Vault
pip install dotzen[vault]      # HashiCorp Vault
pip install dotzen[cloud]      # All cloud providers

# File formats
pip install dotzen[yaml]       # YAML support (PyYAML)
pip install dotzen[toml]       # TOML support
pip install dotzen[json5]      # JSON5 support
pip install dotzen[formats]    # All formats

# Development
pip install dotzen[dev]        # Testing and dev tools
pip install dotzen[docs]       # Documentation building
pip install dotzen[test]       # Testing with cloud mocks

# Everything
pip install dotzen[all]        # All features
```

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Development Setup

```bash
# Clone the repository
git clone https://github.com/carrington-dev/dotzen.git
cd dotzen

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev,test,all]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Run type checking
mypy dotzen

# Format code
black dotzen tests
ruff check dotzen tests
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=dotzen --cov-report=html

# Run specific test file
pytest tests/test_dotzen.py

# Run with verbose output
pytest -v

# Run only fast tests (skip cloud integration)
pytest -m "not integration"
```

### Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Format code (`black .` and `ruff check --fix .`)
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

Please use our [PR templates](.github/PULL_REQUEST_TEMPLATE/) for:
- 🐛 [Bug fixes](.github/PULL_REQUEST_TEMPLATE/bug.md)
- ✨ [New features](.github/PULL_REQUEST_TEMPLATE/feature.md)
- 📝 [Documentation](.github/PULL_REQUEST_TEMPLATE/docs.md)

---

## 📝 License

DotZen is released under the **MIT License**. See [LICENSE](LICENSE) for details.

```
MIT License

Copyright (c) 2025 Carrington Muleya

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 🙏 Acknowledgments

- Inspired by the [12-factor app methodology](https://12factor.net/)
- Built with insights from ["Design Patterns" by Gang of Four](https://en.wikipedia.org/wiki/Design_Patterns)
- Thanks to all [contributors](https://github.com/carrington-dev/dotzen/graphs/contributors)

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/carrington-dev/dotzen?style=social)
![GitHub forks](https://img.shields.io/github/forks/carrington-dev/dotzen?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/carrington-dev/dotzen?style=social)
![GitHub contributors](https://img.shields.io/github/contributors/carrington-dev/dotzen)
![GitHub last commit](https://img.shields.io/github/last-commit/carrington-dev/dotzen)
![GitHub issues](https://img.shields.io/github/issues/carrington-dev/dotzen)
![GitHub pull requests](https://img.shields.io/github/issues-pr/carrington-dev/dotzen)

---

## 🔗 Links & Resources

- 📦 **PyPI Package**: [pypi.org/project/dotzen](https://pypi.org/project/dotzen/)
- 📚 **Documentation**: [dotzen.readthedocs.io](https://dotzen.readthedocs.io)
- 💻 **Source Code**: [github.com/carrington-dev/dotzen](https://github.com/carrington-dev/dotzen)
- 🐛 **Issue Tracker**: [github.com/carrington-dev/dotzen/issues](https://github.com/carrington-dev/dotzen/issues)
- 💬 **Discussions**: [github.com/carrington-dev/dotzen/discussions](https://github.com/carrington-dev/dotzen/discussions)
- 📝 **Changelog**: [CHANGELOG.md](CHANGELOG.md)
- 🤝 **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 💬 Community & Support

- 🌟 **Star** this repository if you find it helpful
- 🐛 **Report bugs** via [GitHub Issues](https://github.com/carrington-dev/dotzen/issues)
- 💡 **Request features** in [Discussions](https://github.com/carrington-dev/dotzen/discussions)
- 📧 **Contact**: carrington.muleya@outlook.com
- 🐦 **Twitter**: [@carrington_dev](https://twitter.com/carrington_dev) (if applicable)

---

<div align="center">

**Made with 🧘 and ❤️ by [Carrington Muleya](https://github.com/carrington-dev)**

**Find your configuration zen. Try DotZen today!**

[⬆ Back to Top](#-dotzen)

</div>
# 🧘 DotZen

**Peaceful, type-safe Python configuration that just works.**

[![PyPI version](https://badge.fury.io/py/dotzen.svg)](https://badge.fury.io/py/dotzen)
[![Python Support](https://img.shields.io/pypi/pyversions/dotzen.svg)](https://pypi.org/project/dotzen/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/dotzen)](https://pepy.tech/project/dotzen)

DotZen brings zen to Python configuration management. Load settings from environment variables, files, or cloud providers with automatic type casting, validation, and a beautiful fluent API. No more config chaos—just pure zen.

## ✨ Why DotZen?

**Traditional configuration is stressful:**
- 😫 Scattered config sources (env vars, files, secrets)
- 🔢 Type conversion headaches (strings everywhere!)
- 💥 No validation until runtime failures
- 🔁 Duplicated code across projects
- 🔓 Security risks with hardcoded secrets

**DotZen brings peace through:**
- 🎯 **Unified API** - One interface for all config sources
- 🛡️ **Type Safety** - Automatic casting with validation
- 🌐 **Multi-Source** - Environment, files, cloud secrets, Docker
- ✅ **Validation** - Catch errors early, not in production
- 🏗️ **Design Patterns** - Built on proven patterns (Strategy, Builder, Chain of Responsibility)
- 🪶 **Zero Core Dependencies** - Lightweight and fast
- 🔌 **Extensible** - Easy custom sources and validators

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

# With additional format support
pip install dotzen[yaml]       # YAML support
pip install dotzen[toml]       # TOML support
pip install dotzen[all]        # Everything
```

### Simple Usage

```python
from dotzen import

# Automatic type casting
DEBUG = config('DEBUG', cast=bool)
PORT = config('PORT', default=8000, cast=int)
DATABASE_URL = config('DATABASE_URL')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=list)
```

### Builder Pattern (Advanced)

```python
from dotzen import ConfigBuilder

config = (ConfigBuilder()
    .add_environment('APP_')      # Environment variables with prefix
    .add_dotenv('.env')            # .env file
    .add_json('config.json')       # JSON config
    .add_secrets('/run/secrets')   # Docker secrets
    .build())

# Type-safe access
debug = config.get_bool('DEBUG', default=False)
port = config.get_int('PORT', default=8000)
hosts = config.get_list('ALLOWED_HOSTS')
```

## 🎯 Key Features

### 🔄 Multi-Source Priority Chain

Configuration sources are checked in order until a value is found:

1. **Environment variables** (highest priority)
2. **.env files**
3. **JSON/YAML files**
4. **Cloud secrets** (AWS, GCP, Azure)
5. **Docker secrets**
6. **Default values** (lowest priority)

### 🎨 Beautiful Fluent API

```python
config = (ConfigBuilder()
    .add_environment()
    .add_dotenv()
    .add_json('settings.json')
    .with_validator(URLValidator('DATABASE_URL'))
    .with_type('MAX_CONNECTIONS', int)
    .build())
```

### 🛡️ Type Safety & Casting

```python
# Automatic type conversion
DEBUG = config.get_bool('DEBUG')                    # bool
PORT = config.get_int('PORT', default=8000)         # int
TIMEOUT = config.get_float('TIMEOUT', default=30.0) # float
HOSTS = config.get_list('ALLOWED_HOSTS')            # list
```

Boolean conversion supports multiple formats:
- `True`: "true", "yes", "1", "on", "t", "y"
- `False`: "false", "no", "0", "off", "f", "n"

### 🌐 Cloud-Native Support

```python
from dotzen import ConfigBuilder

# AWS Secrets Manager
config = (ConfigBuilder()
    .add_aws_secrets('prod/myapp')
    .build())

# Google Cloud Secret Manager
config = (ConfigBuilder()
    .add_gcp_secrets('projects/my-project')
    .build())

# Azure Key Vault
config = (ConfigBuilder()
    .add_azure_keyvault('https://myvault.vault.azure.net')
    .build())
```

### ✅ Built-in Validation

```python
from dotzen.validators import URLValidator, RangeValidator, RegexValidator

config = (ConfigBuilder()
    .add_environment()
    .with_validator(URLValidator('DATABASE_URL'))
    .with_validator(RangeValidator('PORT', 1024, 65535))
    .with_validator(RegexValidator('API_KEY', r'^[A-Za-z0-9]{32}$'))
    .build())
```

## 📚 Use Cases

### Django Settings

```python
from dotzen import

# settings.py
DEBUG = config('DEBUG', cast=bool, default=False)
SECRET_KEY = config('SECRET_KEY')

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

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=list, default=[])
```

### FastAPI Application

```python
from fastapi import FastAPI
from dotzen import ConfigBuilder

config = (ConfigBuilder()
    .add_environment()
    .add_dotenv()
    .build())

app = FastAPI(
    debug=config.get_bool('DEBUG', False),
    title=config('APP_NAME', 'My API'),
)

@app.get("/config")
def get_config():
    return {
        "environment": config('ENVIRONMENT', 'development'),
        "version": config('VERSION', '1.0.0'),
    }
```

### Microservices with Docker

```python
# docker-compose.yml provides secrets in /run/secrets/
config = (ConfigBuilder()
    .add_environment()
    .add_secrets('/run/secrets')
    .add_dotenv('.env')
    .build())

# Access Docker secrets seamlessly
db_password = config('db_password')
api_key = config('api_key')
```

### Multi-Environment Setup

```python
# Loads different configs based on environment
import os
from dotzen import ConfigBuilder

env = os.getenv('ENVIRONMENT', 'development')

config = (ConfigBuilder()
    .add_environment()
    .add_dotenv(f'.env.{env}')      # .env.development, .env.production
    .add_json(f'config.{env}.json')
    .build())
```

## 🏗️ Design Patterns

DotZen is built on proven software design patterns:

- **Strategy Pattern** - Pluggable configuration sources
- **Chain of Responsibility** - Priority-based value resolution
- **Builder Pattern** - Fluent configuration construction
- **Factory Pattern** - Auto-detection of config files
- **Singleton Pattern** - Global config instance
- **Facade Pattern** - Simplified user interface
- **Null Object Pattern** - Graceful handling of missing sources

## 🆚 Comparison with Alternatives

| Feature | DotZen | python-decouple | pydantic-settings | dynaconf |
|---------|--------|-----------------|-------------------|----------|
| Type Safety | ✅ Full | ⚠️ Basic | ✅ Full | ✅ Full |
| Cloud Secrets | ✅ Yes | ❌ No | ⚠️ Limited | ✅ Yes |
| Fluent API | ✅ Yes | ❌ No | ❌ No | ⚠️ Limited |
| Validation | ✅ Yes | ⚠️ Basic | ✅ Yes | ✅ Yes |
| Zero Core Deps | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| Modern Design | ✅ Yes | ❌ No | ✅ Yes | ⚠️ Limited |
| Multi-Source | ✅ Yes | ⚠️ Limited | ⚠️ Limited | ✅ Yes |

## 🎓 Documentation

Full documentation is available at [dotzen.readthedocs.io](https://dotzen.readthedocs.io)

## 📦 Extras

Install optional dependencies for additional features:

```bash
pip install dotzen[aws]        # AWS Secrets Manager
pip install dotzen[gcp]        # Google Cloud Secret Manager
pip install dotzen[azure]      # Azure Key Vault
pip install dotzen[vault]      # HashiCorp Vault
pip install dotzen[yaml]       # YAML file support
pip install dotzen[toml]       # TOML file support
pip install dotzen[cloud]      # All cloud providers
pip install dotzen[formats]    # All file formats
pip install dotzen[all]        # Everything
```

## 🤝 Contributing

Contributions are welcome! Please see our [Contributing Guide](https://github.com/carrington-dev/dotzen/blob/main/CONTRIBUTING.md) for details.

## 📄 License

DotZen is released under the MIT License. See the [LICENSE](https://github.com/carrington-dev/dotzen/blob/main/LICENSE) file for details.

## 🙏 Credits

Created with 🧘 by [Carrington Muleya](https://github.com/carrington-dev)

## 🔗 Links

- **PyPI**: [pypi.org/project/dotzen](https://pypi.org/project/dotzen/)
- **Documentation**: [dotzen.readthedocs.io](https://dotzen.readthedocs.io)
- **Source Code**: [github.com/carrington-dev/dotzen](https://github.com/carrington-dev/dotzen)
- **Issue Tracker**: [github.com/carrington-dev/dotzen/issues](https://github.com/carrington-dev/dotzen/issues)

---

**Find your configuration zen. Try DotZen today! 🧘✨**
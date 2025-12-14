```markdown
# Quick Start

Get up and running with DotZen in 5 minutes.

## Installation

```bash
# Core library (zero dependencies)
pip install dotzen

# With cloud provider support
pip install dotzen[all]
```

## Basic Usage

### Simple Configuration

```python
from dotzen import config

# Get configuration values with automatic type casting
API_KEY = config('API_KEY')
DEBUG = config('DEBUG', cast=bool, default=False)
MAX_CONNECTIONS = config('MAX_CONNECTIONS', cast=int, default=100)
ALLOWED_ORIGINS = config('ALLOWED_ORIGINS', cast=list)
```

### Using the Builder Pattern

```python
from dotzen import ConfigBuilder

# Build a configuration with multiple sources
config = (ConfigBuilder()
    .add_environment('APP_')        # Env vars with prefix
    .add_dotenv('.env')             # .env file
    .add_json('config.json')        # JSON config
    .add_secrets('/run/secrets')    # Docker secrets
    .build())

# Type-safe access
debug = config.get_bool('DEBUG', default=False)
port = config.get_int('PORT', default=8000)
hosts = config.get_list('ALLOWED_HOSTS')
```

## Your First Project

### 1. Create a `.env` file

```bash
# .env
DEBUG=true
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
MAX_CONNECTIONS=50
```

### 2. Create your configuration

```python
# config.py
from dotzen import ConfigBuilder

config = (ConfigBuilder()
    .add_environment()
    .add_dotenv('.env')
    .build())

# Export configuration values
DEBUG = config.get_bool('DEBUG')
DATABASE_URL = config('DATABASE_URL')
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config.get_list('ALLOWED_HOSTS')
MAX_CONNECTIONS = config.get_int('MAX_CONNECTIONS')
```

### 3. Use in your application

```python
# app.py
from config import DEBUG, DATABASE_URL, ALLOWED_HOSTS

if DEBUG:
    print(f"Running in DEBUG mode")
    print(f"Database: {DATABASE_URL}")
    print(f"Allowed hosts: {ALLOWED_HOSTS}")
```

## Common Patterns

### Django Settings

```python
from dotzen import config

DEBUG = config('DEBUG', cast=bool, default=False)
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=list, default=[])

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
    title=config('APP_NAME', default='My API'),
    debug=config.get_bool('DEBUG', default=False),
)

@app.get("/")
def read_root():
    return {
        "environment": config('ENVIRONMENT', default='development'),
        "version": config('VERSION', default='1.0.0'),
    }
```

### Flask Application

```python
from flask import Flask
from dotzen import config

app = Flask(__name__)
app.config['DEBUG'] = config('DEBUG', cast=bool, default=False)
app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
```

## Next Steps

- Learn about [Configuration Sources](configuration_sources.md)
- Explore [Type Casting](type_casting.md)
- Add [Validation](validation.md)
- Use [Cloud Secrets](cloud_secrets.md)
- Study [Design Patterns](design_patterns.md)
- Check out more [Examples](examples.md)
```

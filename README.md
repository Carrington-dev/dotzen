# DotZen - Find Your Configuration Zen

## Tagline
**Peaceful, type-safe Python configuration that just works.**

---

## Short Description (PyPI/GitHub)
DotZen is a modern, type-safe Python configuration library that gracefully loads settings from multiple sources (environment variables, .env files, JSON, YAML, cloud secrets) with elegant validation and zero stress. Embrace the zen of clean configuration management.

---

## Elevator Pitch (30 seconds)
DotZen brings peace to Python configuration management. Load settings from anywhere—environment variables, files, or cloud providers—with automatic type casting, validation, and a beautiful fluent API. No more config chaos, just pure zen.

---

## Detailed Description

### What is DotZen?

DotZen is a **modern Python configuration library** designed with simplicity, type safety, and flexibility in mind. It provides a unified, elegant interface for loading configuration from multiple sources while maintaining strict separation between your code and configuration data—following the principles of 12-factor apps.

### Why DotZen?

**Traditional configuration management is stressful:**
- Scattered config sources (env vars, files, secrets managers)
- Type conversion headaches (strings everywhere)
- No validation until runtime failures
- Duplicated code across projects
- Security risks with hardcoded secrets

**DotZen brings peace through:**
- **Unified API** - One simple interface for all config sources
- **Type Safety** - Automatic casting with Pydantic support
- **Multi-Source** - Environment, files, cloud secrets, Docker
- **Validation** - Catch config errors early, not in production
- **Design Patterns** - Built on proven patterns (Strategy, Builder, Chain of Responsibility)
- **Zero Dependencies** - Core functionality with no required deps
- **Extensible** - Easy to add custom sources and validators

### Key Features

**Beautiful Fluent API**
```python
config = (ConfigBuilder()
    .add_environment()
    .add_dotenv()
    .add_json('settings.json')
    .build())
```

**Multi-Source Priority Chain**
Environment variables → .env files → JSON/YAML → Cloud secrets → Defaults

**Type-Safe with Auto-Casting**
```python
DEBUG = config.get_bool('DEBUG', default=False)
PORT = config.get_int('PORT', default=8000)
HOSTS = config.get_list('ALLOWED_HOSTS')
```

**Cloud-Native Support**
- AWS Secrets Manager
- Google Cloud Secret Manager
- Azure Key Vault
- HashiCorp Vault
- Docker Secrets

**Built-in Validation**
```python
builder.with_validator(RangeValidator('PORT', 1024, 65535))
builder.with_validator(URLValidator('DATABASE_URL'))
```

**Security First**
- Secret encryption/decryption
- Sensitive data redaction in logs
- No secrets in version control
- Secure defaults

**Framework Integrations**
- Django settings loader
- FastAPI dependency injection
- Flask config support
- Pydantic BaseSettings

### Perfect For

- **Microservices** - Consistent config across services
- **12-Factor Apps** - Strict code/config separation
- **Multi-Environment** - Dev, staging, production configs
- **Cloud Deployments** - Native cloud secrets support
- **Team Projects** - Standardized config approach
- **Production Apps** - Validated, type-safe configuration

### Design Philosophy

**Peaceful Configuration**
Configuration should be straightforward, not a source of stress. DotZen provides sensible defaults, clear error messages, and intuitive APIs.

**Type Safety Without Complexity**
Get the benefits of type checking without verbose schemas or complex setups. Types are inferred naturally.

**Progressive Disclosure**
Start simple with `config('KEY')`, grow into advanced features (validation, encryption, multi-source) as needed.

**Fail Fast, Fail Clear**
Configuration errors should be caught at startup with clear, actionable error messages—not mysteriously in production.

**Separation of Concerns**
Keep configuration separate from code. No hardcoded values, environment-specific logic, or secrets in repositories.

### Technical Highlights

**Architecture**
Built on proven design patterns:
- Strategy Pattern for config sources
- Chain of Responsibility for priority resolution
- Builder Pattern for fluent construction
- Factory Pattern for auto-detection
- Facade Pattern for simple API

**Performance**
- Intelligent caching reduces file/API calls
- Lazy loading for optional sources
- Minimal overhead (less than 1ms config access)

**Quality**
- Greater than 95% test coverage
- Type hints throughout
- Comprehensive documentation
- Production-tested

### Comparison with Alternatives

| Feature | DotZen | python-decouple | pydantic-settings | dynaconf |
|---------|--------|-----------------|-------------------|----------|
| Type Safety | Full | Basic | Full | Full |
| Cloud Secrets | Yes | No | Limited | Yes |
| Fluent API | Yes | No | No | Limited |
| Validation | Yes | Basic | Yes | Yes |
| Zero Deps | Yes | Yes | No | No |
| Modern Design | Yes | No | Yes | Limited |

### Use Cases

**Startup Configuration**
```python
from dotzen import config

# Automatic source detection
DEBUG = config('DEBUG', cast=bool)
DATABASE_URL = config('DATABASE_URL')
SECRET_KEY = config('SECRET_KEY')
```

**Advanced Multi-Source**
```python
config = (ConfigBuilder()
    .add_environment('APP_')
    .add_dotenv('.env')
    .add_json('config.json')
    .add_aws_secrets('prod/myapp')
    .with_validator(URLValidator('DATABASE_URL'))
    .build())
```

**Pydantic Integration**
```python
from dotzen.pydantic import BaseSettings

class Settings(BaseSettings):
    debug: bool = False
    database_url: str
    api_key: str
    
settings = Settings()
```

**Django Settings**
```python
from dotzen import config

DEBUG = config('DEBUG', cast=bool)
SECRET_KEY = config('SECRET_KEY')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'HOST': config('DB_HOST'),
        'PORT': config.get_int('DB_PORT', 5432),
    }
}
```

### Who Should Use DotZen?

**Ideal candidates:**
- Projects requiring type-safe configuration
- Applications deployed to cloud environments
- Teams valuing clean, maintainable code
- Systems needing multi-source config flexibility
- Applications following 12-factor app principles
- Projects requiring validated, secure configuration

### Community & Support

- **Documentation**: https://dotzen.readthedocs.io
- **Discussions**: GitHub Discussions
- **Issues**: GitHub Issues
- **PyPI**: `pip install dotzen`
- **GitHub**: github.com/carrington-dev/dotzen

---

## One-Liner Descriptions

**Ultra-short (Twitter/social):**
Type-safe Python configuration from any source. Environment variables, files, cloud secrets—all with one clean API.

**Short (GitHub bio):**
Modern, type-safe Python configuration library. Load settings from env vars, files, or cloud providers with elegant validation.

**Medium (README subtitle):**
DotZen provides peaceful, type-safe configuration management for Python applications. Load from environment variables, .env files, JSON, YAML, or cloud secret managers with automatic validation and type casting.

**SEO-focused:**
Python configuration library with type safety, multi-source loading (environment variables, .env, JSON, YAML), cloud secrets support (AWS, GCP, Azure), Pydantic integration, and automatic validation for modern applications.

---

## Marketing Angles

### For Developers
Stop fighting with configuration. DotZen gives you type-safe settings that just work.

### For Teams
Standardize configuration across your entire stack. One library, consistent patterns, happy developers.

### For DevOps
Deploy with confidence. Cloud-native secrets, environment-aware configs, zero hardcoded values.

### For Startups
Move fast without breaking things. DotZen catches config errors before they reach production.

### For Enterprise
Production-ready configuration management with validation, audit trails, and multi-environment support.

---

## Keywords (for SEO/Discovery)

**Primary:**
- Python configuration
- Configuration management
- Type-safe config
- Settings management
- Environment variables

**Secondary:**
- .env file parser
- Cloud secrets
- AWS Secrets Manager
- Configuration validation
- 12-factor app
- Pydantic settings
- Django settings
- FastAPI config

**Technical:**
- python-decouple alternative
- dynaconf alternative
- Configuration library
- Settings loader
- Config parser
- Type casting
- Multi-source configuration

---

## Taglines (Alternative Options)

1. **Find Your Configuration Zen** (Current)
2. Configuration Without the Chaos
3. Peaceful Python Configuration
4. Type-Safe Config That Just Works
5. Your Path to Configuration Enlightenment
6. Clean Config, Clear Mind
7. Configuration Done Right
8. The Zen of Python Configuration
9. Stress-Free Settings Management
10. Configuration Nirvana for Python

---

**License:** MIT  
**Python Support:** 3.8+ | 3.9 | 3.10 | 3.11 | 3.12 | 3.13  
**Status:** Production Ready  
**Maintenance:** Actively Maintained
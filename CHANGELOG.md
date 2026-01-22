# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Additional cloud provider integrations
- Enhanced validation capabilities
- Performance optimizations for large configuration sets

---

## [1.1.0] - 2026-01-21

### Added
- Full test suite implementation with comprehensive coverage
- Enhanced type safety features across all configuration sources
- Improved error handling and validation mechanisms
- Additional convenience methods for common configuration patterns
- Extended documentation with real-world examples

### Changed
- Updated core dependencies to latest stable versions
- Improved ConfigBuilder fluent API design
- Enhanced cloud secrets integration reliability
- Optimized configuration loading performance

### Fixed
- Resolved all test suite failures
- Fixed edge cases in type casting for complex data types
- Improved error messages for better debugging experience
- Corrected validation behavior for nested configuration values

### Documentation
- Added comprehensive Django, FastAPI, and Flask integration examples
- Expanded architecture and design patterns documentation
- Improved installation and quick start guides
- Added troubleshooting section to documentation

---

## [1.0.0] - 2025-12-15

### Added
- Initial stable release of DotZen
- Core configuration management functionality
- Multi-source configuration support:
  - Environment variables
  - .env files
  - JSON files
  - YAML files
  - TOML files
  - Docker secrets
- Cloud provider integrations:
  - AWS Secrets Manager
  - Google Cloud Secret Manager
  - Azure Key Vault
  - HashiCorp Vault
- Type-safe configuration with automatic casting:
  - Boolean conversion
  - Integer conversion
  - Float conversion
  - List conversion
- Built-in validation framework:
  - URL validation
  - Range validation
  - Regex validation
  - Custom validators
- Design pattern implementations:
  - Strategy pattern for config sources
  - Chain of Responsibility for source priority
  - Builder pattern for fluent API
  - Factory pattern for auto-detection
  - Singleton pattern for global config
  - Facade pattern for simple interface
- ConfigBuilder with fluent API
- ConfigFactory for auto-detection
- ConfigSingleton for application-wide access
- Zero core dependencies (optional extras for features)

### Documentation
- Complete README with examples
- Full API documentation
- Contribution guidelines
- Architecture documentation
- Comparison with alternatives

---

## [0.9.0] - 2025-11-20

### Added
- Beta release with core functionality
- Basic environment variable support
- .env file loading
- JSON configuration support
- Simple type casting
- ConfigBuilder pattern implementation

### Changed
- Refactored core architecture for better extensibility
- Improved error handling

### Fixed
- Various bug fixes from alpha testing

---

## [0.5.0] - 2025-10-15

### Added
- Alpha release
- Proof of concept implementation
- Basic configuration loading
- Initial documentation

---

## [0.1.0] - 2025-09-01

### Added
- Project initialization
- Basic project structure
- Initial README and documentation

---

## Migration Guides

### Upgrading to 1.1.0 from 1.0.0

No breaking changes. This is a minor release with improvements and bug fixes. Simply update your dependency:

```bash
pip install --upgrade dotzen
```

### Upgrading to 1.0.0 from 0.x

Version 1.0.0 introduced some API changes for better consistency:

#### Breaking Changes

1. **ConfigBuilder method names**:
   ```python
   # Old (0.x)
   builder.add_env()
   builder.add_env_file('.env')
   
   # New (1.0.0+)
   builder.add_environment()
   builder.add_dotenv('.env')
   ```

2. **Validator interface**:
   ```python
   # Old (0.x)
   def validator(value):
       return is_valid(value)
   
   # New (1.0.0+)
   def validator(key: str, value: Any):
       if not is_valid(value):
           raise ValidationError(f"{key} is invalid")
   ```

3. **Exception hierarchy**:
   - `ConfigError` is now the base exception
   - `UndefinedValueError` replaces `MissingValueError`
   - `ValidationError` is now separate from `ValueError`

---

## Version History Summary

| Version | Release Date | Status | Notable Features |
|---------|-------------|--------|------------------|
| 1.1.0 | 2026-01-21 | Current | Full test coverage, improved stability |
| 1.0.0 | 2025-12-15 | Stable | Initial stable release, all core features |
| 0.9.0 | 2025-11-20 | Beta | Feature complete beta |
| 0.5.0 | 2025-10-15 | Alpha | Proof of concept |
| 0.1.0 | 2025-09-01 | Initial | Project start |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## Support

- 📦 [PyPI Package](https://pypi.org/project/dotzen/)
- 📚 [Documentation](https://dotzen.readthedocs.io)
- 💻 [GitHub Repository](https://github.com/carrington-dev/dotzen)
- 🐛 [Issue Tracker](https://github.com/carrington-dev/dotzen/issues)

---

[Unreleased]: https://github.com/carrington-dev/dotzen/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/carrington-dev/dotzen/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/carrington-dev/dotzen/compare/v0.9.0...v1.0.0
[0.9.0]: https://github.com/carrington-dev/dotzen/compare/v0.5.0...v0.9.0
[0.5.0]: https://github.com/carrington-dev/dotzen/compare/v0.1.0...v0.5.0
[0.1.0]: https://github.com/carrington-dev/dotzen/releases/tag/v0.1.0
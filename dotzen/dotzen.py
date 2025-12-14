"""
DotZen - Peaceful, type-safe Python configuration library
Implements multiple design patterns for flexible configuration management
"""
import os
import json
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type, TypeVar, Union, List, Callable
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

# Type variables for generic typing
T = TypeVar('T')


# ============================================================================
# EXCEPTIONS
# ============================================================================

class ConfigError(Exception):
    """Base exception for configuration errors"""
    pass


class UndefinedValueError(ConfigError):
    """Raised when a required configuration value is not found"""
    pass


class ValidationError(ConfigError):
    """Raised when configuration validation fails"""
    pass


class SourceNotFoundError(ConfigError):
    """Raised when configuration source is not found"""
    pass


# ============================================================================
# SENTINEL PATTERN - Marker for undefined values
# ============================================================================

class _Undefined:
    """Sentinel class to represent undefined values"""
    def __repr__(self) -> str:
        return "<UNDEFINED>"

UNDEFINED = _Undefined()


# ============================================================================
# STRATEGY PATTERN - Different configuration sources
# ============================================================================

class ConfigSource(ABC):
    """
    Abstract base class for configuration sources (Strategy Pattern)
    Defines interface that all concrete sources must implement
    """
    
    @abstractmethod
    def load(self) -> Dict[str, str]:
        """Load configuration from source"""
        pass
    
    @abstractmethod
    def exists(self) -> bool:
        """Check if source exists"""
        pass
    
    def get(self, key: str, default: Any = UNDEFINED) -> Any:
        """Get a value from the loaded configuration"""
        data = self.load()
        if key in data:
            return data[key]
        if default is not UNDEFINED:
            return default
        raise UndefinedValueError(f"Key '{key}' not found in configuration")


class EnvironmentSource(ConfigSource):
    """Load configuration from environment variables"""
    
    def __init__(self, prefix: Optional[str] = None):
        self.prefix = prefix
    
    def load(self) -> Dict[str, str]:
        if self.prefix:
            return {
                k.replace(self.prefix, '', 1): v 
                for k, v in os.environ.items() 
                if k.startswith(self.prefix)
            }
        return dict(os.environ)
    
    def exists(self) -> bool:
        return True  # Environment always exists


class DotEnvSource(ConfigSource):
    """Load configuration from .env files"""
    
    def __init__(self, filepath: Union[str, Path] = ".env", encoding: str = "utf-8"):
        self.filepath = Path(filepath)
        self.encoding = encoding
        self._cache: Optional[Dict[str, str]] = None
    
    def load(self) -> Dict[str, str]:
        if self._cache is not None:
            return self._cache
        
        if not self.exists():
            return {}
        
        data = {}
        with open(self.filepath, 'r', encoding=self.encoding) as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if not line or line.startswith('#') or '=' not in line:
                    continue
                
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # Remove quotes
                if len(value) >= 2 and value[0] in ('"', "'") and value[-1] == value[0]:
                    value = value[1:-1]
                
                data[key] = value
        
        self._cache = data
        return data
    
    def exists(self) -> bool:
        return self.filepath.exists()


class JsonSource(ConfigSource):
    """Load configuration from JSON files"""
    
    def __init__(self, filepath: Union[str, Path], encoding: str = "utf-8"):
        self.filepath = Path(filepath)
        self.encoding = encoding
        self._cache: Optional[Dict[str, str]] = None
    
    def load(self) -> Dict[str, str]:
        if self._cache is not None:
            return self._cache
        
        if not self.exists():
            return {}
        
        with open(self.filepath, 'r', encoding=self.encoding) as f:
            data = json.load(f)
        
        # Flatten nested dicts with dot notation
        self._cache = self._flatten_dict(data)
        return self._cache
    
    def _flatten_dict(self, d: Dict, parent_key: str = '', sep: str = '.') -> Dict[str, str]:
        """Flatten nested dictionary"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, str(v)))
        return dict(items)
    
    def exists(self) -> bool:
        return self.filepath.exists()


class SecretSource(ConfigSource):
    """Load configuration from Docker secrets directory"""
    
    def __init__(self, directory: Union[str, Path] = "/run/secrets"):
        self.directory = Path(directory)
        self._cache: Optional[Dict[str, str]] = None
    
    def load(self) -> Dict[str, str]:
        if self._cache is not None:
            return self._cache
        
        if not self.exists():
            return {}
        
        data = {}
        for secret_file in self.directory.iterdir():
            if secret_file.is_file():
                with open(secret_file, 'r') as f:
                    data[secret_file.name] = f.read().strip()
        
        self._cache = data
        return data
    
    def exists(self) -> bool:
        return self.directory.exists() and self.directory.is_dir()


# NULL OBJECT PATTERN
class NullSource(ConfigSource):
    """Null object that returns empty configuration"""
    
    def load(self) -> Dict[str, str]:
        return {}
    
    def exists(self) -> bool:
        return False


# ============================================================================
# CHAIN OF RESPONSIBILITY PATTERN - Cascading config lookup
# ============================================================================

class ConfigChain:
    """
    Chain of Responsibility Pattern - tries sources in order until value found
    """
    
    def __init__(self, sources: List[ConfigSource]):
        self.sources = sources
    
    def get(self, key: str, default: Any = UNDEFINED) -> Any:
        """Try each source in order"""
        for source in self.sources:
            try:
                return source.get(key, UNDEFINED)
            except UndefinedValueError:
                continue
        
        # No source had the value
        if default is not UNDEFINED:
            return default
        
        raise UndefinedValueError(
            f"Key '{key}' not found in any configuration source"
        )


# ============================================================================
# BUILDER PATTERN - Fluent interface for configuration
# ============================================================================

class ConfigBuilder:
    """
    Builder Pattern - constructs Config with fluent interface
    """
    
    def __init__(self):
        self._sources: List[ConfigSource] = []
        self._validators: List[Callable] = []
        self._type_casters: Dict[str, Type] = {}
    
    def add_environment(self, prefix: Optional[str] = None) -> 'ConfigBuilder':
        """Add environment variables as source"""
        self._sources.append(EnvironmentSource(prefix))
        return self
    
    def add_dotenv(self, filepath: str = ".env") -> 'ConfigBuilder':
        """Add .env file as source"""
        self._sources.append(DotEnvSource(filepath))
        return self
    
    def add_json(self, filepath: str) -> 'ConfigBuilder':
        """Add JSON file as source"""
        self._sources.append(JsonSource(filepath))
        return self
    
    def add_secrets(self, directory: str = "/run/secrets") -> 'ConfigBuilder':
        """Add Docker secrets as source"""
        self._sources.append(SecretSource(directory))
        return self
    
    def add_custom_source(self, source: ConfigSource) -> 'ConfigBuilder':
        """Add custom configuration source"""
        self._sources.append(source)
        return self
    
    def with_validator(self, validator: Callable) -> 'ConfigBuilder':
        """Add validation function"""
        self._validators.append(validator)
        return self
    
    def with_type(self, key: str, type_class: Type) -> 'ConfigBuilder':
        """Define type casting for specific key"""
        self._type_casters[key] = type_class
        return self
    
    def build(self) -> 'Config':
        """Build the final Config object"""
        if not self._sources:
            self._sources.append(NullSource())
        
        return Config(
            chain=ConfigChain(self._sources),
            validators=self._validators,
            type_casters=self._type_casters
        )


# ============================================================================
# TYPE CASTING - Support for different data types
# ============================================================================

class TypeCaster:
    """Handles type casting with validation"""
    
    @staticmethod
    def to_bool(value: Any) -> bool:
        """Convert value to boolean"""
        if isinstance(value, bool):
            return value
        
        if isinstance(value, str):
            lower_val = value.lower()
            if lower_val in ('true', 'yes', '1', 'on', 't', 'y'):
                return True
            if lower_val in ('false', 'no', '0', 'off', 'f', 'n'):
                return False
        
        raise ValidationError(f"Cannot convert '{value}' to boolean")
    
    @staticmethod
    def to_int(value: Any) -> int:
        """Convert value to integer"""
        try:
            return int(value)
        except (ValueError, TypeError) as e:
            raise ValidationError(f"Cannot convert '{value}' to integer: {e}")
    
    @staticmethod
    def to_float(value: Any) -> float:
        """Convert value to float"""
        try:
            return float(value)
        except (ValueError, TypeError) as e:
            raise ValidationError(f"Cannot convert '{value}' to float: {e}")
    
    @staticmethod
    def to_list(value: Any, delimiter: str = ',') -> List[str]:
        """Convert value to list"""
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return [item.strip() for item in value.split(delimiter)]
        raise ValidationError(f"Cannot convert '{value}' to list")


# ============================================================================
# FACADE PATTERN - Simplified interface for users
# ============================================================================

class Config:
    """
    Main configuration class (Facade Pattern)
    Provides simple interface to complex configuration system
    """
    
    def __init__(
        self, 
        chain: ConfigChain,
        validators: Optional[List[Callable]] = None,
        type_casters: Optional[Dict[str, Type]] = None
    ):
        self.chain = chain
        self.validators = validators or []
        self.type_casters = type_casters or {}
    
    def get(
        self, 
        key: str, 
        default: Any = UNDEFINED, 
        cast: Optional[Type[T]] = None
    ) -> T:
        """
        Get configuration value with optional type casting
        
        Args:
            key: Configuration key
            default: Default value if key not found
            cast: Type to cast the value to (bool, int, float, str, list)
        
        Returns:
            Configuration value, optionally cast to specified type
        """
        # Get raw value
        value = self.chain.get(key, default)
        
        # Apply type casting
        if cast is not None:
            value = self._cast_value(value, cast)
        elif key in self.type_casters:
            value = self._cast_value(value, self.type_casters[key])
        
        # Run validators
        for validator in self.validators:
            validator(key, value)
        
        return value
    
    def _cast_value(self, value: Any, target_type: Type[T]) -> T:
        """Cast value to target type"""
        if target_type is bool:
            return TypeCaster.to_bool(value)
        elif target_type is int:
            return TypeCaster.to_int(value)
        elif target_type is float:
            return TypeCaster.to_float(value)
        elif target_type is list:
            return TypeCaster.to_list(value)
        elif target_type is str:
            return str(value)
        else:
            return target_type(value)
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """Convenience method for boolean values"""
        return self.get(key, default, cast=bool)
    
    def get_int(self, key: str, default: int = 0) -> int:
        """Convenience method for integer values"""
        return self.get(key, default, cast=int)
    
    def get_float(self, key: str, default: float = 0.0) -> float:
        """Convenience method for float values"""
        return self.get(key, default, cast=float)
    
    def get_list(self, key: str, default: Optional[List] = None) -> List:
        """Convenience method for list values"""
        return self.get(key, default or [], cast=list)
    
    def __call__(self, *args, **kwargs):
        """Allow Config to be called like a function"""
        return self.get(*args, **kwargs)


# ============================================================================
# FACTORY PATTERN - Auto-detect configuration files
# ============================================================================

class ConfigFactory:
    """
    Factory Pattern - creates Config with auto-detected sources
    """
    
    SUPPORTED_FILES = {
        '.env': DotEnvSource,
        'config.json': JsonSource,
        'settings.json': JsonSource,
    }
    
    @classmethod
    def auto_config(
        cls, 
        search_path: Optional[Path] = None,
        include_environment: bool = True
    ) -> Config:
        """
        Auto-detect and load configuration from common locations
        """
        if search_path is None:
            search_path = Path.cwd()
        
        builder = ConfigBuilder()
        
        # Always check environment first (highest priority)
        if include_environment:
            builder.add_environment()
        
        # Search for config files
        for filename, source_class in cls.SUPPORTED_FILES.items():
            filepath = search_path / filename
            if filepath.exists():
                if source_class == DotEnvSource:
                    builder.add_dotenv(str(filepath))
                elif source_class == JsonSource:
                    builder.add_json(str(filepath))
        
        return builder.build()


# ============================================================================
# SINGLETON PATTERN - Global config instance
# ============================================================================

class ConfigSingleton:
    """
    Singleton Pattern - provides global config instance
    """
    _instance: Optional[Config] = None
    
    @classmethod
    def get_instance(cls) -> Config:
        """Get or create singleton instance"""
        if cls._instance is None:
            cls._instance = ConfigFactory.auto_config()
        return cls._instance
    
    @classmethod
    def reset(cls):
        """Reset singleton (useful for testing)"""
        cls._instance = None


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

# Global config instance (Singleton)
_global_config = ConfigSingleton.get_instance()


def config(key: str, default: Any = UNDEFINED, cast: Optional[Type] = None) -> Any:
    """
    Convenience function for getting config values
    
    Usage:
        DEBUG = config('DEBUG', default=False, cast=bool)
        DATABASE_URL = config('DATABASE_URL')
        PORT = config('PORT', default=8000, cast=int)
    """
    return _global_config.get(key, default, cast)


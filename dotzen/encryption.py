"""
DotZen Encryption Module - Secure configuration value encryption/decryption
"""
import base64
import hashlib
from abc import ABC, abstractmethod
from typing import Optional, Type, Dict


# ============================================================================
# ENCRYPTION STRATEGIES
# ============================================================================

class EncryptionStrategy(ABC):
    """Abstract base class for encryption strategies (Strategy Pattern)"""
    
    @abstractmethod
    def encrypt(self, value: str) -> str:
        """Encrypt a value"""
        pass
    
    @abstractmethod
    def decrypt(self, encrypted_value: str) -> str:
        """Decrypt a value"""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the encryption algorithm"""
        pass


class Base64Strategy(EncryptionStrategy):
    """Base64 encoding/decoding strategy"""
    
    def encrypt(self, value: str) -> str:
        """Encode value to base64"""
        return base64.b64encode(value.encode('utf-8')).decode('utf-8')
    
    def decrypt(self, encrypted_value: str) -> str:
        """Decode value from base64"""
        try:
            return base64.b64decode(encrypted_value.encode('utf-8')).decode('utf-8')
        except Exception as e:
            raise ValueError(f"Failed to decode base64 value: {e}")
    
    @property
    def name(self) -> str:
        return "base64"


class MD5Strategy(EncryptionStrategy):
    """
    MD5 hashing strategy (one-way only)
    Note: This is for hashing, not encryption. Values cannot be decrypted.
    """
    
    def encrypt(self, value: str) -> str:
        """Hash value using MD5"""
        return hashlib.md5(value.encode('utf-8')).hexdigest()
    
    def decrypt(self, encrypted_value: str) -> str:
        """MD5 is one-way, cannot decrypt"""
        raise NotImplementedError(
            "MD5 is a one-way hash function and cannot be decrypted. "
            "Use it only for comparison purposes."
        )
    
    @property
    def name(self) -> str:
        return "md5"


class SHA256Strategy(EncryptionStrategy):
    """
    SHA256 hashing strategy (one-way only)
    Note: This is for hashing, not encryption. Values cannot be decrypted.
    """
    
    def encrypt(self, value: str) -> str:
        """Hash value using SHA256"""
        return hashlib.sha256(value.encode('utf-8')).hexdigest()
    
    def decrypt(self, encrypted_value: str) -> str:
        """SHA256 is one-way, cannot decrypt"""
        raise NotImplementedError(
            "SHA256 is a one-way hash function and cannot be decrypted. "
            "Use it only for comparison purposes."
        )
    
    @property
    def name(self) -> str:
        return "sha256"


class FernetStrategy(EncryptionStrategy):
    """
    Fernet symmetric encryption (requires cryptography package)
    This is proper encryption with a secret key.
    """
    
    def __init__(self, secret_key: Optional[bytes] = None):
        """
        Initialize Fernet encryption
        
        Args:
            secret_key: Encryption key (32 url-safe base64-encoded bytes)
                       If not provided, a new key will be generated
        """
        try:
            from cryptography.fernet import Fernet
        except ImportError:
            raise ImportError(
                "cryptography package is required for Fernet encryption. "
                "Install it with: pip install cryptography"
            )
        
        if secret_key is None:
            secret_key = Fernet.generate_key()
        
        self.fernet = Fernet(secret_key)
        self.secret_key = secret_key
    
    def encrypt(self, value: str) -> str:
        """Encrypt value using Fernet"""
        encrypted = self.fernet.encrypt(value.encode('utf-8'))
        return encrypted.decode('utf-8')
    
    def decrypt(self, encrypted_value: str) -> str:
        """Decrypt value using Fernet"""
        try:
            decrypted = self.fernet.decrypt(encrypted_value.encode('utf-8'))
            return decrypted.decode('utf-8')
        except Exception as e:
            raise ValueError(f"Failed to decrypt Fernet value: {e}")
    
    @property
    def name(self) -> str:
        return "fernet"
    
    def get_key(self) -> bytes:
        """Get the encryption key"""
        return self.secret_key


# ============================================================================
# ENCRYPTION MANAGER
# ============================================================================

class EncryptionManager:
    """
    Manages encryption strategies and provides easy access to them
    """
    
    # Registry of available strategies
    _strategies: Dict[str, Type[EncryptionStrategy]] = {
        'base64': Base64Strategy,
        'md5': MD5Strategy,
        'sha256': SHA256Strategy,
    }
    
    # Default strategy
    DEFAULT_ALGORITHM = 'base64'
    
    @classmethod
    def register_strategy(cls, name: str, strategy_class: Type[EncryptionStrategy]):
        """Register a custom encryption strategy"""
        cls._strategies[name.lower()] = strategy_class
    
    @classmethod
    def get_strategy(cls, algorithm: str = None, **kwargs) -> EncryptionStrategy:
        """
        Get an encryption strategy instance
        
        Args:
            algorithm: Algorithm name (base64, md5, sha256, fernet)
            **kwargs: Additional arguments for strategy initialization
        """
        if algorithm is None:
            algorithm = cls.DEFAULT_ALGORITHM
        
        algorithm = algorithm.lower()
        
        # Special handling for Fernet
        if algorithm == 'fernet':
            return FernetStrategy(**kwargs)
        
        if algorithm not in cls._strategies:
            available = ', '.join(cls._strategies.keys())
            raise ValueError(
                f"Unknown encryption algorithm '{algorithm}'. "
                f"Available: {available}, fernet"
            )
        
        strategy_class = cls._strategies[algorithm]
        return strategy_class(**kwargs)
    
    @classmethod
    def encrypt(cls, value: str, algorithm: str = None, **kwargs) -> str:
        """Convenience method to encrypt a value"""
        strategy = cls.get_strategy(algorithm, **kwargs)
        return strategy.encrypt(value)
    
    @classmethod
    def decrypt(cls, encrypted_value: str, algorithm: str = None, **kwargs) -> str:
        """Convenience method to decrypt a value"""
        strategy = cls.get_strategy(algorithm, **kwargs)
        return strategy.decrypt(encrypted_value)


# ============================================================================
# SECURE CONFIG WRAPPER
# ============================================================================

class SecureConfig:
    """
    Wrapper around Config that adds encryption/decryption support
    """
    
    def __init__(self, config, default_algorithm: str = 'base64', encryption_key: Optional[bytes] = None):
        """
        Initialize SecureConfig
        
        Args:
            config: The underlying Config instance
            default_algorithm: Default encryption algorithm to use
            encryption_key: Secret key for algorithms that require it (e.g., Fernet)
        """
        self.config = config
        self.default_algorithm = default_algorithm
        self.encryption_key = encryption_key
        self._encryption_manager = EncryptionManager()
    
    def konfig(
        self, 
        key: str, 
        default: any = None,
        cast: Optional[Type] = None,
        encrypted: bool = True,
        algorithm: Optional[str] = None
    ) -> any:
        """
        Get configuration value with automatic decryption
        
        Args:
            key: Configuration key
            default: Default value if not found
            cast: Type to cast the decrypted value to
            encrypted: Whether the value is encrypted (default: True)
            algorithm: Encryption algorithm to use for decryption
        
        Returns:
            Decrypted configuration value
        
        Example:
            SECRET_KEY = secure_config.konfig('SECRET_KEY')
            API_KEY = secure_config.konfig('API_KEY', algorithm='fernet')
        """
        # Get the raw (encrypted) value
        try:
            raw_value = self.config.get(key)
        except:
            if default is not None:
                return default
            raise
        
        # If not encrypted, return as-is
        if not encrypted:
            if cast:
                return self.config.get(key, default, cast)
            return raw_value
        
        # Decrypt the value
        algo = algorithm or self.default_algorithm
        kwargs = {}
        if algo == 'fernet' and self.encryption_key:
            kwargs['secret_key'] = self.encryption_key
        
        try:
            decrypted = self._encryption_manager.decrypt(raw_value, algo, **kwargs)
        except Exception as e:
            if default is not None:
                return default
            raise ValueError(f"Failed to decrypt '{key}': {e}")
        
        # Apply type casting if needed
        if cast:
            from dotzen.dotzen import TypeCaster
            if cast is bool:
                return TypeCaster.to_bool(decrypted)
            elif cast is int:
                return TypeCaster.to_int(decrypted)
            elif cast is float:
                return TypeCaster.to_float(decrypted)
            elif cast is list:
                return TypeCaster.to_list(decrypted)
            else:
                return cast(decrypted)
        
        return decrypted
    
    def encrypt_value(self, value: str, algorithm: Optional[str] = None) -> str:
        """
        Encrypt a value for storage in configuration
        
        Args:
            value: Value to encrypt
            algorithm: Encryption algorithm to use
        
        Returns:
            Encrypted value
        
        Example:
            encrypted = secure_config.encrypt_value('my-secret-key')
            # Store 'encrypted' in your .env file
        """
        algo = algorithm or self.default_algorithm
        kwargs = {}
        if algo == 'fernet' and self.encryption_key:
            kwargs['secret_key'] = self.encryption_key
        
        return self._encryption_manager.encrypt(value, algo, **kwargs)


# ============================================================================
# CONVENIENCE FUNCTION
# ============================================================================

def konfig(
    key: str,
    default: any = None,
    cast: Optional[Type] = None,
    encrypted: bool = True,
    algorithm: str = 'base64',
    config_instance = None
) -> any:
    """
    Convenience function for getting encrypted configuration values
    
    Args:
        key: Configuration key
        default: Default value if not found
        cast: Type to cast the decrypted value to
        encrypted: Whether the value is encrypted (default: True)
        algorithm: Encryption algorithm to use
        config_instance: Config instance to use (uses global if None)
    
    Returns:
        Decrypted configuration value
    
    Example:
        from dotzen.encryption import konfig
        from dotzen import ConfigBuilder
        
        # Create a proper config instance
        config_inst = ConfigBuilder().add_environment().build()
        SECRET_KEY = konfig('SECRET_KEY', config_instance=config_inst)
        
        # Or for quick use (uses global singleton)
        API_KEY = konfig('API_KEY', algorithm='fernet')
        DEBUG = konfig('DEBUG', cast=bool, encrypted=False)
    """
    if config_instance is None:
        # Import here to avoid circular imports
        from dotzen.dotzen import ConfigSingleton
        config_instance = ConfigSingleton.get_instance()
    
    # If config_instance is a function (the global config convenience function),
    # get the actual Config instance instead
    if callable(config_instance) and hasattr(config_instance, '__name__') and config_instance.__name__ == 'config':
        from dotzen.dotzen import ConfigSingleton
        config_instance = ConfigSingleton.get_instance()
    
    secure_config = SecureConfig(config_instance, default_algorithm=algorithm)
    return secure_config.konfig(key, default, cast, encrypted, algorithm)


# ============================================================================
# CLI HELPER FOR ENCRYPTION
# ============================================================================

def encrypt_for_env(value: str, algorithm: str = 'base64', show_key: bool = False) -> str:
    """
    Helper function to encrypt values for .env files
    
    Args:
        value: Value to encrypt
        algorithm: Algorithm to use
        show_key: For Fernet, whether to display the encryption key
    
    Returns:
        Encrypted value
    
    Example:
        >>> from dotzen.encryption import encrypt_for_env
        >>> encrypted = encrypt_for_env('my-secret-password')
        >>> print(f"SECRET_KEY={encrypted}")
        SECRET_KEY=bXktc2VjcmV0LXBhc3N3b3Jk
    """
    if algorithm == 'fernet':
        strategy = FernetStrategy()
        encrypted = strategy.encrypt(value)
        if show_key:
            print(f"\n⚠️  Save this encryption key securely!")
            print(f"ENCRYPTION_KEY={strategy.get_key().decode('utf-8')}\n")
        return encrypted
    else:
        return EncryptionManager.encrypt(value, algorithm)
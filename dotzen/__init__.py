__version__ = "1.0.0"
__author__ = "Carrington Muleya"
__name__ = "dotzen"


from .dotzen import ConfigBuilder, ConfigFactory, config
from .encryption import (
    konfig,
    SecureConfig,
    EncryptionManager,
    EncryptionStrategy,
    Base64Strategy,
    MD5Strategy,
    SHA256Strategy,
    FernetStrategy,
    encrypt_for_env,
)

__all__ = [
    # Core functionality
    'ConfigBuilder',
    'ConfigFactory',
    'config',
    
    # Encryption functionality
    'konfig',
    'SecureConfig',
    'EncryptionManager',
    'EncryptionStrategy',
    'Base64Strategy',
    'MD5Strategy',
    'SHA256Strategy',
    'FernetStrategy',
    'encrypt_for_env',
]

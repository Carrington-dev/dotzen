"""
DotZen Encryption - Complete Usage Examples
"""

import os
from dotzen import ConfigBuilder, konfig, SecureConfig, encrypt_for_env, EncryptionManager


# ============================================================================
# Example 1: Basic Usage with konfig() function
# ============================================================================

def example1_basic_konfig():
    """Simple encrypted configuration retrieval"""
    print("=== Example 1: Basic konfig() Usage ===\n")
    
    # Set up environment with encrypted values
    # Original: "my-secret-key"
    # Encrypted (base64): "bXktc2VjcmV0LWtleQ=="
    os.environ['SECRET_KEY'] = 'bXktc2VjcmV0LWtleQ=='
    os.environ['API_KEY'] = 'c3VwZXItc2VjcmV0LWFwaS1rZXk='  # "super-secret-api-key"
    
    # Retrieve and automatically decrypt
    secret_key = konfig('SECRET_KEY')
    api_key = konfig('API_KEY')
    
    print(f"SECRET_KEY (encrypted): {os.environ['SECRET_KEY']}")
    print(f"SECRET_KEY (decrypted): {secret_key}")
    print()
    print(f"API_KEY (encrypted): {os.environ['API_KEY']}")
    print(f"API_KEY (decrypted): {api_key}")
    print()


# ============================================================================
# Example 2: Using Different Encryption Algorithms
# ============================================================================

def example2_different_algorithms():
    """Using MD5 and SHA256 for password hashing"""
    print("=== Example 2: Different Algorithms ===\n")
    
    # Base64 (reversible encryption)
    original = "my-password"
    base64_encrypted = EncryptionManager.encrypt(original, 'base64')
    base64_decrypted = EncryptionManager.decrypt(base64_encrypted, 'base64')
    
    print("Base64 (Reversible):")
    print(f"  Original:  {original}")
    print(f"  Encrypted: {base64_encrypted}")
    print(f"  Decrypted: {base64_decrypted}")
    print()
    
    # MD5 (one-way hash)
    md5_hash = EncryptionManager.encrypt(original, 'md5')
    print("MD5 (One-way hash):")
    print(f"  Original: {original}")
    print(f"  Hashed:   {md5_hash}")
    print("  (Cannot be decrypted)")
    print()
    
    # SHA256 (one-way hash)
    sha256_hash = EncryptionManager.encrypt(original, 'sha256')
    print("SHA256 (One-way hash):")
    print(f"  Original: {original}")
    print(f"  Hashed:   {sha256_hash}")
    print("  (Cannot be decrypted)")
    print()


# ============================================================================
# Example 3: Using SecureConfig with ConfigBuilder
# ============================================================================

def example3_secure_config_builder():
    """Using SecureConfig with the Builder pattern"""
    print("=== Example 3: SecureConfig with Builder ===\n")
    
    # Create a .env file with encrypted values
    env_content = """
# Regular values
DEBUG=true
PORT=8000

# Encrypted values (base64)
DATABASE_PASSWORD=cGFzc3dvcmQxMjM=
JWT_SECRET=c3VwZXItc2VjcmV0LWp3dC10b2tlbg==
STRIPE_KEY=c2tfdGVzdF8xMjM0NTY3ODkw
"""
    
    with open('.env.encrypted', 'w') as f:
        f.write(env_content)
    
    # Build config
    config = (ConfigBuilder()
              .add_environment()
              .add_dotenv('.env.encrypted')
              .build())
    
    # Wrap with SecureConfig
    secure_config = SecureConfig(config, default_algorithm='base64')
    
    # Get regular (non-encrypted) values
    debug = secure_config.konfig('DEBUG', cast=bool, encrypted=False)
    port = secure_config.konfig('PORT', cast=int, encrypted=False)
    
    # Get encrypted values (automatically decrypted)
    db_password = secure_config.konfig('DATABASE_PASSWORD')
    jwt_secret = secure_config.konfig('JWT_SECRET')
    stripe_key = secure_config.konfig('STRIPE_KEY')
    
    print("Regular values:")
    print(f"  DEBUG: {debug}")
    print(f"  PORT: {port}")
    print()
    print("Encrypted values (decrypted):")
    print(f"  DATABASE_PASSWORD: {db_password}")
    print(f"  JWT_SECRET: {jwt_secret}")
    print(f"  STRIPE_KEY: {stripe_key}")
    print()
    
    # Cleanup
    os.remove('.env.encrypted')


# ============================================================================
# Example 4: Encrypting Values for .env Files
# ============================================================================

def example4_encrypt_for_env():
    """How to encrypt values before storing in .env"""
    print("=== Example 4: Encrypt Values for .env ===\n")
    
    # Values to encrypt
    secrets = {
        'DATABASE_PASSWORD': 'postgres_password_123',
        'API_KEY': 'sk_live_abcdefghijklmnop',
        'JWT_SECRET': 'my-super-secret-jwt-token',
        'STRIPE_SECRET': 'sk_test_1234567890',
    }
    
    print("Add these to your .env file:\n")
    for key, value in secrets.items():
        encrypted = encrypt_for_env(value, algorithm='base64')
        print(f"{key}={encrypted}")
    
    print("\n# Original values (for reference):")
    for key, value in secrets.items():
        print(f"# {key}={value}")
    print()


# ============================================================================
# Example 5: Django Settings with Encrypted Values
# ============================================================================

def example5_django_settings():
    """Example Django settings.py with encrypted config"""
    print("=== Example 5: Django Settings ===\n")
    
    # Simulate .env with encrypted values
    os.environ['SECRET_KEY'] = 'ZGphbmdvLWluc2VjdXJlLXNlY3JldC1rZXk='  # base64
    os.environ['DATABASE_PASSWORD'] = 'bXlkYnBhc3N3b3Jk'  # "mydbpassword"
    os.environ['EMAIL_PASSWORD'] = 'ZW1haWxwYXNzMTIz'  # "emailpass123"
    os.environ['DEBUG'] = 'false'
    
    # settings.py equivalent
    print("# settings.py")
    print("from dotzen import konfig, ConfigBuilder, SecureConfig\n")
    print("config = ConfigBuilder().add_environment().build()")
    print("secure = SecureConfig(config)\n")
    
    # Get values
    SECRET_KEY = konfig('SECRET_KEY')
    DEBUG = konfig('DEBUG', cast=bool, encrypted=False)
    DB_PASSWORD = konfig('DATABASE_PASSWORD')
    EMAIL_PASSWORD = konfig('EMAIL_PASSWORD')
    
    print(f"SECRET_KEY = '{SECRET_KEY}'")
    print(f"DEBUG = {DEBUG}")
    print()
    print("DATABASES = {")
    print("    'default': {")
    print("        'ENGINE': 'django.db.backends.postgresql',")
    print(f"        'PASSWORD': '{DB_PASSWORD}',")
    print("    }")
    print("}")
    print()
    print(f"EMAIL_HOST_PASSWORD = '{EMAIL_PASSWORD}'")
    print()


# ============================================================================
# Example 6: Type Casting with Encrypted Values
# ============================================================================

def example6_type_casting():
    """Type casting with encrypted values"""
    print("=== Example 6: Type Casting ===\n")
    
    # Set up encrypted values
    os.environ['MAX_CONNECTIONS'] = 'NTA='  # "50" in base64
    os.environ['ALLOWED_HOSTS'] = 'bG9jYWxob3N0LDEyNy4wLjAuMSxleGFtcGxlLmNvbQ=='  # list
    os.environ['ENABLE_CACHE'] = 'dHJ1ZQ=='  # "true" in base64
    
    # Retrieve with type casting
    max_conn = konfig('MAX_CONNECTIONS', cast=int)
    hosts = konfig('ALLOWED_HOSTS', cast=list)
    cache_enabled = konfig('ENABLE_CACHE', cast=bool)
    
    print(f"MAX_CONNECTIONS: {max_conn} (type: {type(max_conn).__name__})")
    print(f"ALLOWED_HOSTS: {hosts} (type: {type(hosts).__name__})")
    print(f"ENABLE_CACHE: {cache_enabled} (type: {type(cache_enabled).__name__})")
    print()


# ============================================================================
# Example 7: CLI Tool for Encrypting Values
# ============================================================================

def example7_cli_tool():
    """Command-line tool example for encrypting secrets"""
    print("=== Example 7: CLI Encryption Tool ===\n")
    
    print("# Create a simple CLI tool:")
    print("""
# encrypt_secret.py
import sys
from dotzen import encrypt_for_env

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python encrypt_secret.py <value> [algorithm]")
        sys.exit(1)
    
    value = sys.argv[1]
    algorithm = sys.argv[2] if len(sys.argv) > 2 else 'base64'
    
    encrypted = encrypt_for_env(value, algorithm)
    print(f"Encrypted: {encrypted}")
""")
    
    print("\n# Usage:")
    print("$ python encrypt_secret.py 'my-secret-password'")
    print("Encrypted: bXktc2VjcmV0LXBhc3N3b3Jk")
    print()
    
    # Actually encrypt some values
    print("Example encryptions:")
    examples = [
        'my-api-key-12345',
        'postgres://user:pass@localhost/db',
        'super-secret-jwt-token',
    ]
    
    for val in examples:
        enc = encrypt_for_env(val)
        print(f"  '{val[:20]}...' → {enc[:30]}...")
    print()


# ============================================================================
# Example 8: FastAPI with Encrypted Config
# ============================================================================

def example8_fastapi():
    """FastAPI application with encrypted configuration"""
    print("=== Example 8: FastAPI with Encrypted Config ===\n")
    
    print("""
# main.py
from fastapi import FastAPI, Depends
from dotzen import ConfigBuilder, SecureConfig

# Build secure config
config = ConfigBuilder().add_environment().add_dotenv().build()
secure_config = SecureConfig(config, default_algorithm='base64')

app = FastAPI(
    title="My Secure API",
    debug=secure_config.konfig('DEBUG', cast=bool, encrypted=False)
)

# Dependency for getting secrets
def get_database_password():
    return secure_config.konfig('DATABASE_PASSWORD')

def get_jwt_secret():
    return secure_config.konfig('JWT_SECRET')

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/login")
async def login(
    db_password: str = Depends(get_database_password),
    jwt_secret: str = Depends(get_jwt_secret)
):
    # Use decrypted secrets
    # Connect to database with db_password
    # Sign JWT with jwt_secret
    return {"token": "..."}
""")
    print()


# ============================================================================
# Example 9: Custom Encryption Strategy
# ============================================================================

def example9_custom_strategy():
    """Creating a custom encryption strategy"""
    print("=== Example 9: Custom Encryption Strategy ===\n")
    
    print("""
from dotzen import EncryptionStrategy, EncryptionManager
import base64

class ROT13Strategy(EncryptionStrategy):
    '''Simple ROT13 cipher for demonstration'''
    
    def encrypt(self, value: str) -> str:
        return value.encode('rot13')
    
    def decrypt(self, encrypted_value: str) -> str:
        return encrypted_value.encode('rot13')
    
    @property
    def name(self) -> str:
        return "rot13"

# Register custom strategy
EncryptionManager.register_strategy('rot13', ROT13Strategy)

# Use it
encrypted = EncryptionManager.encrypt('hello', 'rot13')
decrypted = EncryptionManager.decrypt(encrypted, 'rot13')
""")
    print()


# ============================================================================
# Run all examples
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("DotZen Encryption - Complete Usage Examples")
    print("="*70 + "\n")
    
    example1_basic_konfig()
    print("\n" + "-"*70 + "\n")
    
    example2_different_algorithms()
    print("\n" + "-"*70 + "\n")
    
    example3_secure_config_builder()
    print("\n" + "-"*70 + "\n")
    
    example4_encrypt_for_env()
    print("\n" + "-"*70 + "\n")
    
    example5_django_settings()
    print("\n" + "-"*70 + "\n")
    
    example6_type_casting()
    print("\n" + "-"*70 + "\n")
    
    example7_cli_tool()
    print("\n" + "-"*70 + "\n")
    
    example8_fastapi()
    print("\n" + "-"*70 + "\n")
    
    example9_custom_strategy()
    
    print("\n" + "="*70)
    print("✅ All examples completed!")
    print("="*70 + "\n")
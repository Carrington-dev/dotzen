"""
tests/test_encryption.py - Comprehensive tests for encryption feature
"""

import pytest
import os
from dotzen.encryption import (
    Base64Strategy,
    MD5Strategy,
    SHA256Strategy,
    EncryptionManager,
    SecureConfig,
    konfig,
    encrypt_for_env,
)
from dotzen import ConfigBuilder


class TestBase64Strategy:
    """Tests for Base64 encryption strategy"""
    
    def test_encrypt_decrypt_simple(self):
        """Test basic encryption and decryption"""
        strategy = Base64Strategy()
        original = "carrington"
        encrypted = strategy.encrypt(original)
        decrypted = strategy.decrypt(encrypted)
        
        assert encrypted == "Y2FycmluZ3Rvbg=="
        assert decrypted == original
    
    def test_encrypt_decrypt_special_chars(self):
        """Test with special characters"""
        strategy = Base64Strategy()
        original = "p@ssw0rd!#$%"
        encrypted = strategy.encrypt(original)
        decrypted = strategy.decrypt(encrypted)
        
        assert decrypted == original
    
    def test_encrypt_decrypt_unicode(self):
        """Test with unicode characters"""
        strategy = Base64Strategy()
        original = "Hello 世界 🌍"
        encrypted = strategy.encrypt(original)
        decrypted = strategy.decrypt(encrypted)
        
        assert decrypted == original
    
    def test_decrypt_invalid_base64(self):
        """Test decrypting invalid base64"""
        strategy = Base64Strategy()
        with pytest.raises(ValueError):
            strategy.decrypt("not-valid-base64!@#")
    
    def test_name_property(self):
        """Test strategy name"""
        strategy = Base64Strategy()
        assert strategy.name == "base64"


class TestMD5Strategy:
    """Tests for MD5 hashing strategy"""
    
    def test_encrypt_consistent(self):
        """Test MD5 hashing is consistent"""
        strategy = MD5Strategy()
        value = "password123"
        hash1 = strategy.encrypt(value)
        hash2 = strategy.encrypt(value)
        
        assert hash1 == hash2
        assert len(hash1) == 32  # MD5 produces 32-char hex
    
    def test_encrypt_different_values(self):
        """Test different values produce different hashes"""
        strategy = MD5Strategy()
        hash1 = strategy.encrypt("password1")
        hash2 = strategy.encrypt("password2")
        
        assert hash1 != hash2
    
    def test_decrypt_not_supported(self):
        """Test that MD5 decryption raises error"""
        strategy = MD5Strategy()
        hashed = strategy.encrypt("password")
        
        with pytest.raises(NotImplementedError):
            strategy.decrypt(hashed)
    
    def test_name_property(self):
        """Test strategy name"""
        strategy = MD5Strategy()
        assert strategy.name == "md5"


class TestSHA256Strategy:
    """Tests for SHA256 hashing strategy"""
    
    def test_encrypt_consistent(self):
        """Test SHA256 hashing is consistent"""
        strategy = SHA256Strategy()
        value = "secure-password"
        hash1 = strategy.encrypt(value)
        hash2 = strategy.encrypt(value)
        
        assert hash1 == hash2
        assert len(hash1) == 64  # SHA256 produces 64-char hex
    
    def test_encrypt_different_values(self):
        """Test different values produce different hashes"""
        strategy = SHA256Strategy()
        hash1 = strategy.encrypt("password1")
        hash2 = strategy.encrypt("password2")
        
        assert hash1 != hash2
    
    def test_decrypt_not_supported(self):
        """Test that SHA256 decryption raises error"""
        strategy = SHA256Strategy()
        hashed = strategy.encrypt("password")
        
        with pytest.raises(NotImplementedError):
            strategy.decrypt(hashed)
    
    def test_name_property(self):
        """Test strategy name"""
        strategy = SHA256Strategy()
        assert strategy.name == "sha256"


class TestEncryptionManager:
    """Tests for EncryptionManager"""
    
    def test_get_strategy_base64(self):
        """Test getting base64 strategy"""
        strategy = EncryptionManager.get_strategy('base64')
        assert isinstance(strategy, Base64Strategy)
    
    def test_get_strategy_md5(self):
        """Test getting md5 strategy"""
        strategy = EncryptionManager.get_strategy('md5')
        assert isinstance(strategy, MD5Strategy)
    
    def test_get_strategy_sha256(self):
        """Test getting sha256 strategy"""
        strategy = EncryptionManager.get_strategy('sha256')
        assert isinstance(strategy, SHA256Strategy)
    
    def test_get_strategy_default(self):
        """Test getting default strategy"""
        strategy = EncryptionManager.get_strategy()
        assert isinstance(strategy, Base64Strategy)
    
    def test_get_strategy_case_insensitive(self):
        """Test strategy names are case insensitive"""
        strategy1 = EncryptionManager.get_strategy('BASE64')
        strategy2 = EncryptionManager.get_strategy('Base64')
        
        assert isinstance(strategy1, Base64Strategy)
        assert isinstance(strategy2, Base64Strategy)
    
    def test_get_strategy_invalid(self):
        """Test invalid strategy raises error"""
        with pytest.raises(ValueError, match="Unknown encryption algorithm"):
            EncryptionManager.get_strategy('invalid')
    
    def test_encrypt_convenience_method(self):
        """Test convenience encrypt method"""
        encrypted = EncryptionManager.encrypt("test", 'base64')
        assert encrypted == "dGVzdA=="
    
    def test_decrypt_convenience_method(self):
        """Test convenience decrypt method"""
        decrypted = EncryptionManager.decrypt("dGVzdA==", 'base64')
        assert decrypted == "test"


class TestSecureConfig:
    """Tests for SecureConfig"""
    
    def setup_method(self):
        """Set up test environment"""
        os.environ.clear()
    
    def test_konfig_encrypted_value(self):
        """Test getting encrypted configuration value"""
        os.environ['SECRET_KEY'] = 'bXktc2VjcmV0LWtleQ=='  # "my-secret-key" in base64
        
        config = ConfigBuilder().add_environment().build()
        secure_config = SecureConfig(config)
        
        value = secure_config.konfig('SECRET_KEY')
        assert value == "my-secret-key"
    
    def test_konfig_non_encrypted_value(self):
        """Test getting non-encrypted value"""
        os.environ['DEBUG'] = 'true'
        
        config = ConfigBuilder().add_environment().build()
        secure_config = SecureConfig(config)
        
        value = secure_config.konfig('DEBUG', encrypted=False)
        assert value == "true"
    
    def test_konfig_with_type_casting(self):
        """Test konfig with type casting"""
        os.environ['PORT'] = 'ODA4MA=='  # "8080" in base64
        
        config = ConfigBuilder().add_environment().build()
        secure_config = SecureConfig(config)
        
        value = secure_config.konfig('PORT', cast=int)
        assert value == 8080
        assert isinstance(value, int)
    
    def test_konfig_with_default(self):
        """Test konfig with default value"""
        config = ConfigBuilder().add_environment().build()
        secure_config = SecureConfig(config)
        
        value = secure_config.konfig('MISSING_KEY', default='default-value')
        assert value == "default-value"
    
    def test_konfig_different_algorithm(self):
        """Test konfig with different algorithm"""
        os.environ['API_KEY'] = 'bXktYXBpLWtleQ=='  # base64
        
        config = ConfigBuilder().add_environment().build()
        secure_config = SecureConfig(config)
        
        value = secure_config.konfig('API_KEY', algorithm='base64')
        assert value == "my-api-key"
    
    def test_encrypt_value(self):
        """Test encrypting value"""
        config = ConfigBuilder().build()
        secure_config = SecureConfig(config)
        
        encrypted = secure_config.encrypt_value("test-value")
        assert encrypted == "dGVzdC12YWx1ZQ=="
    
    def test_konfig_bool_casting(self):
        """Test boolean type casting"""
        os.environ['ENABLE_FEATURE'] = 'dHJ1ZQ=='  # "true" in base64
        
        config = ConfigBuilder().add_environment().build()
        secure_config = SecureConfig(config)
        
        value = secure_config.konfig('ENABLE_FEATURE', cast=bool)
        assert value is True
    
    def test_konfig_list_casting(self):
        """Test list type casting"""
        os.environ['HOSTS'] = 'bG9jYWxob3N0LDEyNy4wLjAuMQ=='  # "localhost,127.0.0.1"
        
        config = ConfigBuilder().add_environment().build()
        secure_config = SecureConfig(config)
        
        value = secure_config.konfig('HOSTS', cast=list)
        assert value == ['localhost', '127.0.0.1']


class TestKonfigFunction:
    """Tests for konfig() convenience function"""
    
    def setup_method(self):
        """Set up test environment"""
        os.environ.clear()
    
    def test_konfig_basic(self):
        """Test basic konfig usage"""
        os.environ['TEST_KEY'] = 'dGVzdC12YWx1ZQ=='  # "test-value"
        
        value = konfig('TEST_KEY')
        assert value == "test-value"
    
    def test_konfig_with_cast(self):
        """Test konfig with type casting"""
        os.environ['NUMBER'] = 'NDI='  # "42"
        
        value = konfig('NUMBER', cast=int)
        assert value == 42
        assert isinstance(value, int)
    
    def test_konfig_non_encrypted(self):
        """Test konfig with non-encrypted value"""
        os.environ['PLAIN'] = 'plain-text'
        
        value = konfig('PLAIN', encrypted=False)
        assert value == "plain-text"
    
    def test_konfig_different_algorithm(self):
        """Test konfig with different algorithm"""
        os.environ['SECRET'] = 'c2VjcmV0'  # "secret" in base64
        
        value = konfig('SECRET', algorithm='base64')
        assert value == "secret"


class TestEncryptForEnv:
    """Tests for encrypt_for_env helper"""
    
    def test_encrypt_base64(self):
        """Test encrypting for env with base64"""
        encrypted = encrypt_for_env("my-password", algorithm='base64')
        assert encrypted == "bXktcGFzc3dvcmQ="
    
    def test_encrypt_md5(self):
        """Test encrypting for env with md5"""
        hashed = encrypt_for_env("password123", algorithm='md5')
        assert len(hashed) == 32  # MD5 hash length
    
    def test_encrypt_sha256(self):
        """Test encrypting for env with sha256"""
        hashed = encrypt_for_env("password123", algorithm='sha256')
        assert len(hashed) == 64  # SHA256 hash length


class TestIntegration:
    """Integration tests combining multiple features"""
    
    def setup_method(self):
        """Set up test environment"""
        os.environ.clear()
        # Clean up any test files
        if os.path.exists('.env.test'):
            os.remove('.env.test')
    
    def teardown_method(self):
        """Clean up after tests"""
        if os.path.exists('.env.test'):
            os.remove('.env.test')
    
    def test_full_workflow(self):
        """Test complete workflow: encrypt -> store -> retrieve -> decrypt"""
        # Step 1: Encrypt values
        secrets = {
            'API_KEY': 'secret-api-key-12345',
            'DB_PASSWORD': 'postgres_pass_123',
            'JWT_SECRET': 'jwt-token-secret',
        }
        
        encrypted_secrets = {}
        for key, value in secrets.items():
            encrypted_secrets[key] = encrypt_for_env(value)
        
        # Step 2: Write to .env file
        with open('.env.test', 'w') as f:
            for key, encrypted in encrypted_secrets.items():
                f.write(f"{key}={encrypted}\n")
        
        # Step 3: Load configuration
        config = ConfigBuilder().add_dotenv('.env.test').build()
        secure_config = SecureConfig(config)
        
        # Step 4: Retrieve and verify
        for key, original_value in secrets.items():
            decrypted = secure_config.konfig(key)
            assert decrypted == original_value
    
    def test_mixed_encrypted_plain(self):
        """Test mix of encrypted and plain values"""
        with open('.env.test', 'w') as f:
            f.write("DEBUG=true\n")
            f.write("PORT=8000\n")
            f.write("SECRET_KEY=bXktc2VjcmV0\n")  # "my-secret" encrypted
            f.write("API_KEY=YXBpLWtleQ==\n")  # "api-key" encrypted
        
        config = ConfigBuilder().add_dotenv('.env.test').build()
        secure_config = SecureConfig(config)
        
        # Plain values
        debug = secure_config.konfig('DEBUG', encrypted=False)
        port = secure_config.konfig('PORT', cast=int, encrypted=False)
        
        # Encrypted values
        secret = secure_config.konfig('SECRET_KEY')
        api_key = secure_config.konfig('API_KEY')
        
        assert debug == "true"
        assert port == 8000
        assert secret == "my-secret"
        assert api_key == "api-key"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
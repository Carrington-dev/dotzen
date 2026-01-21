"""
Tests for ConfigFactory and convenience functions
"""

import pytest
import os
import json
import tempfile
from pathlib import Path
from dotzen.dotzen import (
    ConfigFactory,
    ConfigSingleton,
    config,
)


class TestConfigFactory:
    """Tests for ConfigFactory"""
    
    def setup_method(self):
        """Set up test environment"""
        os.environ.clear()
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = Path.cwd()
        os.chdir(self.temp_dir)
    
    def teardown_method(self):
        """Clean up temporary files"""
        os.chdir(self.original_cwd)
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_auto_config_with_env_file(self):
        """Test auto_config detects .env file"""
        env_file = Path(self.temp_dir) / '.env'
        env_file.write_text('KEY=value\n')
        
        config = ConfigFactory.auto_config()
        assert config.get('KEY') == 'value'
    
    def test_auto_config_with_config_json(self):
        """Test auto_config detects config.json"""
        json_file = Path(self.temp_dir) / 'config.json'
        json_file.write_text(json.dumps({'key': 'value'}))
        
        config = ConfigFactory.auto_config()
        assert config.get('key') == 'value'
    
    def test_auto_config_with_settings_json(self):
        """Test auto_config detects settings.json"""
        json_file = Path(self.temp_dir) / 'settings.json'
        json_file.write_text(json.dumps({'setting': 'value'}))
        
        config = ConfigFactory.auto_config()
        assert config.get('setting') == 'value'
    
    def test_auto_config_environment_priority(self):
        """Test that environment variables have priority"""
        os.environ['KEY'] = 'from_env'
        env_file = Path(self.temp_dir) / '.env'
        env_file.write_text('KEY=from_file\n')
        
        config = ConfigFactory.auto_config()
        assert config.get('KEY') == 'from_env'
    
    def test_auto_config_custom_search_path(self):
        """Test auto_config with custom search path"""
        custom_dir = Path(self.temp_dir) / 'custom'
        custom_dir.mkdir()
        env_file = custom_dir / '.env'
        env_file.write_text('CUSTOM=value\n')
        
        config = ConfigFactory.auto_config(search_path=custom_dir)
        assert config.get('CUSTOM') == 'value'
    
    def test_auto_config_without_environment(self):
        """Test auto_config excluding environment variables"""
        os.environ['ENV_VAR'] = 'env_value'
        env_file = Path(self.temp_dir) / '.env'
        env_file.write_text('FILE_VAR=file_value\n')
        
        config = ConfigFactory.auto_config(include_environment=False)
        
        # Should not find environment variable
        assert config.get('FILE_VAR') == 'file_value'
        value = config.get('ENV_VAR', default='missing')
        assert value == 'missing'
    
    def test_auto_config_multiple_files(self):
        """Test auto_config with multiple config files"""
        env_file = Path(self.temp_dir) / '.env'
        env_file.write_text('ENV_KEY=env_value\n')
        
        json_file = Path(self.temp_dir) / 'config.json'
        json_file.write_text(json.dumps({'json_key': 'json_value'}))
        
        config = ConfigFactory.auto_config()
        
        assert config.get('ENV_KEY') == 'env_value'
        assert config.get('json_key') == 'json_value'
    
    def test_auto_config_no_files(self):
        """Test auto_config when no config files exist"""
        os.environ['TEST'] = 'value'
        config = ConfigFactory.auto_config()
        
        assert config.get('TEST') == 'value'
        assert config.get('MISSING', default='default') == 'default'


class TestConfigSingleton:
    """Tests for ConfigSingleton"""
    
    def setup_method(self):
        """Set up test environment"""
        os.environ.clear()
        ConfigSingleton.reset()
    
    def teardown_method(self):
        """Clean up singleton"""
        ConfigSingleton.reset()
    
    def test_get_instance_creates_singleton(self):
        """Test get_instance creates singleton"""
        instance1 = ConfigSingleton.get_instance()
        instance2 = ConfigSingleton.get_instance()
        
        assert instance1 is instance2
    
    def test_reset_clears_singleton(self):
        """Test reset clears singleton"""
        instance1 = ConfigSingleton.get_instance()
        ConfigSingleton.reset()
        instance2 = ConfigSingleton.get_instance()
        
        assert instance1 is not instance2


class TestConfigConvenienceFunction:
    """Tests for config() convenience function"""
    
    def setup_method(self):
        """Set up test environment"""
        os.environ.clear()
        ConfigSingleton.reset()
    
    def teardown_method(self):
        """Clean up"""
        ConfigSingleton.reset()
    
    def test_config_function_basic(self):
        """Test basic config() usage"""
        os.environ['APP_NAME'] = 'MyApp'
        value = config('APP_NAME')
        assert value == 'MyApp'
    
    def test_config_function_with_default(self):
        """Test config() with default value"""
        value = config('MISSING_KEY', default='default_value')
        assert value == 'default_value'
    
    def test_config_function_with_cast(self):
        """Test config() with type casting"""
        os.environ['PORT'] = '8080'
        os.environ['DEBUG'] = 'true'
        
        port = config('PORT', cast=int)
        debug = config('DEBUG', cast=bool)
        
        assert port == 8080
        assert isinstance(port, int)
        assert debug is True
        assert isinstance(debug, bool)
    
    def test_config_function_raises_without_default(self):
        """Test config() raises error without default"""
        from dotzen.dotzen import UndefinedValueError
        
        with pytest.raises(UndefinedValueError):
            config('NON_EXISTENT_KEY')
    
    def test_config_function_uses_singleton(self):
        """Test that config() uses singleton instance"""
        os.environ['KEY1'] = 'value1'
        
        # First call
        value1 = config('KEY1')
        
        # Add new environment variable
        os.environ['KEY2'] = 'value2'
        
        # Second call should use same singleton
        value2 = config('KEY2')
        
        assert value1 == 'value1'
        assert value2 == 'value2'


class TestIntegrationScenarios:
    """Integration tests for real-world scenarios"""
    
    def setup_method(self):
        """Set up test environment"""
        os.environ.clear()
        ConfigSingleton.reset()
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = Path.cwd()
        os.chdir(self.temp_dir)
    
    def teardown_method(self):
        """Clean up"""
        os.chdir(self.original_cwd)
        ConfigSingleton.reset()
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_typical_web_app_config(self):
        """Test typical web application configuration"""
        # Create .env file with app config
        env_file = Path(self.temp_dir) / '.env'
        env_file.write_text("""
            # Application settings
            APP_NAME=MyWebApp
            DEBUG=true
            
            # Server settings
            HOST=0.0.0.0
            PORT=8080
            
            # Database
            DATABASE_URL=postgresql://localhost/mydb
            DB_POOL_SIZE=10
            
            # Security
            SECRET_KEY=super-secret-key
            ALLOWED_HOSTS=localhost,127.0.0.1,example.com
        """.strip())
        
        # Override with environment variables (production)
        os.environ['DEBUG'] = 'false'
        os.environ['DATABASE_URL'] = 'postgresql://prod.db.com/mydb'
        
        # Load configuration
        config = ConfigFactory.auto_config()
        
        # Verify configuration
        assert config.get('APP_NAME') == 'MyWebApp'
        assert config.get_bool('DEBUG') is False  # Overridden by environment
        assert config.get('HOST') == '0.0.0.0'
        assert config.get_int('PORT') == 8080
        assert config.get('DATABASE_URL') == 'postgresql://prod.db.com/mydb'
        assert config.get_int('DB_POOL_SIZE') == 10
        assert config.get('SECRET_KEY') == 'super-secret-key'
        assert config.get_list('ALLOWED_HOSTS') == ['localhost', '127.0.0.1', 'example.com']
    
    def test_hierarchical_json_config(self):
        """Test hierarchical JSON configuration"""
        json_file = Path(self.temp_dir) / 'config.json'
        config_data = {
            "app": {
                "name": "MyApp",
                "version": "1.1.0"
            },
            "database": {
                "primary": {
                    "host": "db1.example.com",
                    "port": 5432
                },
                "replica": {
                    "host": "db2.example.com",
                    "port": 5432
                }
            },
            "cache": {
                "redis": {
                    "host": "redis.example.com",
                    "port": 6379
                }
            }
        }
        json_file.write_text(json.dumps(config_data))
        
        config = ConfigFactory.auto_config()
        
        # Access nested values with dot notation
        assert config.get('app.name') == 'MyApp'
        assert config.get('app.version') == '1.1.0'
        assert config.get('database.primary.host') == 'db1.example.com'
        assert config.get_int('database.primary.port') == 5432
        assert config.get('database.replica.host') == 'db2.example.com'
        assert config.get('cache.redis.host') == 'redis.example.com'
        assert config.get_int('cache.redis.port') == 6379
    
    def test_docker_secrets_scenario(self):
        """Test Docker secrets integration"""
        secrets_dir = Path(self.temp_dir) / 'secrets'
        secrets_dir.mkdir()
        
        # Create secrets
        (secrets_dir / 'db_password').write_text('super_secret_password')
        (secrets_dir / 'api_key').write_text('api_key_12345')
        
        # Regular env file for non-sensitive config
        env_file = Path(self.temp_dir) / '.env'
        env_file.write_text('APP_NAME=SecureApp\nDEBUG=false\n')
        
        # Build config with secrets
        from dotzen.dotzen import ConfigBuilder
        config = (ConfigBuilder()
                  .add_environment()
                  .add_dotenv(str(env_file))
                  .add_secrets(str(secrets_dir))
                  .build())
        
        # Verify both regular and secret configs
        assert config.get('APP_NAME') == 'SecureApp'
        assert config.get_bool('DEBUG') is False
        assert config.get('db_password') == 'super_secret_password'
        assert config.get('api_key') == 'api_key_12345'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
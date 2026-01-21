"""
tests/test_config_builder.py - Tests for ConfigBuilder and Config
"""

import pytest
import os
import tempfile
from pathlib import Path
from dotzen.dotzen import (
    ConfigBuilder,
    Config,
    ConfigChain,
    UndefinedValueError,
    ValidationError,
    NullSource,
)


class TestConfigBuilder:
    """Tests for ConfigBuilder"""
    
    def setup_method(self):
        """Set up test environment"""
        os.environ.clear()
        self.temp_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Clean up temporary files"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_builder_creates_config(self):
        """Test that builder creates Config instance"""
        config = ConfigBuilder().build()
        assert isinstance(config, Config)
    
    def test_add_environment(self):
        """Test adding environment source"""
        os.environ['TEST_VAR'] = 'test_value'
        
        config = ConfigBuilder().add_environment().build()
        value = config.get('TEST_VAR')
        
        assert value == 'test_value'
    
    def test_add_environment_with_prefix(self):
        """Test adding environment source with prefix"""
        os.environ['APP_NAME'] = 'myapp'
        os.environ['OTHER_VAR'] = 'other'
        
        config = ConfigBuilder().add_environment(prefix='APP_').build()
        
        assert config.get('NAME') == 'myapp'
        with pytest.raises(UndefinedValueError):
            config.get('OTHER_VAR')
    
    def test_add_dotenv(self):
        """Test adding .env file source"""
        env_file = Path(self.temp_dir) / '.env'
        env_file.write_text('KEY=value\n')
        
        config = ConfigBuilder().add_dotenv(str(env_file)).build()
        value = config.get('KEY')
        
        assert value == 'value'
    
    def test_add_json(self):
        """Test adding JSON file source"""
        import json
        json_file = Path(self.temp_dir) / 'config.json'
        json_file.write_text(json.dumps({'key': 'value'}))
        
        config = ConfigBuilder().add_json(str(json_file)).build()
        value = config.get('key')
        
        assert value == 'value'
    
    def test_add_secrets(self):
        """Test adding secrets directory source"""
        secrets_dir = Path(self.temp_dir) / 'secrets'
        secrets_dir.mkdir()
        (secrets_dir / 'password').write_text('secret123')
        
        config = ConfigBuilder().add_secrets(str(secrets_dir)).build()
        value = config.get('password')
        
        assert value == 'secret123'
    
    def test_add_custom_source(self):
        """Test adding custom source"""
        null_source = NullSource()
        config = ConfigBuilder().add_custom_source(null_source).build()
        
        assert isinstance(config, Config)
    
    def test_fluent_interface(self):
        """Test builder's fluent interface"""
        os.environ['ENV_VAR'] = 'env_value'
        env_file = Path(self.temp_dir) / '.env'
        env_file.write_text('FILE_VAR=file_value\n')
        
        config = (ConfigBuilder()
                  .add_environment()
                  .add_dotenv(str(env_file))
                  .build())
        
        assert config.get('ENV_VAR') == 'env_value'
        assert config.get('FILE_VAR') == 'file_value'
    
    def test_with_validator(self):
        """Test adding validator"""
        def validate_port(key, value):
            if key == 'PORT':
                port = int(value)
                if port < 1 or port > 65535:
                    raise ValidationError("Port must be between 1 and 65535")
        
        os.environ['PORT'] = '8080'
        config = (ConfigBuilder()
                  .add_environment()
                  .with_validator(validate_port)
                  .build())
        
        # Should work fine
        assert config.get('PORT') == '8080'
        
        # Should fail validation
        os.environ['PORT'] = '99999'
        config = (ConfigBuilder()
                  .add_environment()
                  .with_validator(validate_port)
                  .build())
        
        with pytest.raises(ValidationError):
            config.get('PORT')
    
    def test_with_type(self):
        """Test defining type casting for specific key"""
        os.environ['PORT'] = '8080'
        
        config = (ConfigBuilder()
                  .add_environment()
                  .with_type('PORT', int)
                  .build())
        
        value = config.get('PORT')
        assert value == 8080
        assert isinstance(value, int)
    
    def test_build_without_sources_uses_null(self):
        """Test that build without sources uses NullSource"""
        config = ConfigBuilder().build()
        
        # Should not raise, should use default
        value = config.get('MISSING', default='default')
        assert value == 'default'


class TestConfigChain:
    """Tests for ConfigChain (Chain of Responsibility)"""
    
    def setup_method(self):
        """Set up test environment"""
        os.environ.clear()
        self.temp_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Clean up temporary files"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_chain_tries_sources_in_order(self):
        """Test that chain tries sources in order"""
        from dotzen.dotzen import EnvironmentSource, DotEnvSource
        
        os.environ['KEY'] = 'from_env'
        env_file = Path(self.temp_dir) / '.env'
        env_file.write_text('KEY=from_file\n')
        
        # Environment first, then file
        chain = ConfigChain([
            EnvironmentSource(),
            DotEnvSource(env_file)
        ])
        
        # Should get value from first source (environment)
        assert chain.get('KEY') == 'from_env'
    
    def test_chain_falls_through_to_next_source(self):
        """Test that chain falls through to next source"""
        from dotzen.dotzen import EnvironmentSource, DotEnvSource
        
        os.environ['ENV_ONLY'] = 'env_value'
        env_file = Path(self.temp_dir) / '.env'
        env_file.write_text('FILE_ONLY=file_value\n')
        
        chain = ConfigChain([
            EnvironmentSource(),
            DotEnvSource(env_file)
        ])
        
        assert chain.get('ENV_ONLY') == 'env_value'
        assert chain.get('FILE_ONLY') == 'file_value'
    
    def test_chain_with_default(self):
        """Test chain with default value"""
        from dotzen.dotzen import NullSource
        
        chain = ConfigChain([NullSource()])
        value = chain.get('MISSING', default='default')
        
        assert value == 'default'
    
    def test_chain_raises_without_default(self):
        """Test chain raises error when key not found"""
        from dotzen.dotzen import NullSource
        
        chain = ConfigChain([NullSource()])
        
        with pytest.raises(UndefinedValueError):
            chain.get('MISSING')


class TestConfig:
    """Tests for Config class"""
    
    def setup_method(self):
        """Set up test environment"""
        os.environ.clear()
    
    def test_get_simple_value(self):
        """Test getting simple configuration value"""
        os.environ['KEY'] = 'value'
        config = ConfigBuilder().add_environment().build()
        
        assert config.get('KEY') == 'value'
    
    def test_get_with_default(self):
        """Test getting value with default"""
        config = ConfigBuilder().build()
        value = config.get('MISSING', default='default')
        
        assert value == 'default'
    
    def test_get_raises_without_default(self):
        """Test get raises error without default"""
        config = ConfigBuilder().build()
        
        with pytest.raises(UndefinedValueError):
            config.get('MISSING')
    
    def test_get_bool_true_values(self):
        """Test get_bool with true values"""
        config = ConfigBuilder().add_environment().build()
        
        true_values = ['true', 'True', 'TRUE', 'yes', 'Yes', '1', 'on', 't', 'y']
        
        for i, val in enumerate(true_values):
            os.environ[f'BOOL_{i}'] = val
            assert config.get_bool(f'BOOL_{i}') is True
    
    def test_get_bool_false_values(self):
        """Test get_bool with false values"""
        config = ConfigBuilder().add_environment().build()
        
        false_values = ['false', 'False', 'FALSE', 'no', 'No', '0', 'off', 'f', 'n']
        
        for i, val in enumerate(false_values):
            os.environ[f'BOOL_{i}'] = val
            assert config.get_bool(f'BOOL_{i}') is False
    
    def test_get_bool_with_default(self):
        """Test get_bool with default value"""
        config = ConfigBuilder().build()
        
        assert config.get_bool('MISSING', default=True) is True
        assert config.get_bool('MISSING', default=False) is False
    
    def test_get_int(self):
        """Test getting integer value"""
        os.environ['PORT'] = '8080'
        config = ConfigBuilder().add_environment().build()
        
        value = config.get_int('PORT')
        assert value == 8080
        assert isinstance(value, int)
    
    def test_get_int_negative(self):
        """Test getting negative integer"""
        os.environ['TEMP'] = '-10'
        config = ConfigBuilder().add_environment().build()
        
        assert config.get_int('TEMP') == -10
    
    def test_get_int_with_default(self):
        """Test get_int with default"""
        config = ConfigBuilder().build()
        
        assert config.get_int('MISSING', default=42) == 42
    
    def test_get_int_invalid_raises(self):
        """Test get_int with invalid value raises error"""
        os.environ['INVALID'] = 'not_a_number'
        config = ConfigBuilder().add_environment().build()
        
        with pytest.raises(ValidationError):
            config.get_int('INVALID')
    
    def test_get_float(self):
        """Test getting float value"""
        os.environ['PI'] = '3.14159'
        config = ConfigBuilder().add_environment().build()
        
        value = config.get_float('PI')
        assert value == 3.14159
        assert isinstance(value, float)
    
    def test_get_float_with_default(self):
        """Test get_float with default"""
        config = ConfigBuilder().build()
        
        assert config.get_float('MISSING', default=2.5) == 2.5
    
    def test_get_float_invalid_raises(self):
        """Test get_float with invalid value raises error"""
        os.environ['INVALID'] = 'not_a_float'
        config = ConfigBuilder().add_environment().build()
        
        with pytest.raises(ValidationError):
            config.get_float('INVALID')
    
    def test_get_list_comma_separated(self):
        """Test getting list from comma-separated string"""
        os.environ['HOSTS'] = 'localhost,127.0.0.1,example.com'
        config = ConfigBuilder().add_environment().build()
        
        value = config.get_list('HOSTS')
        assert value == ['localhost', '127.0.0.1', 'example.com']
    
    def test_get_list_with_spaces(self):
        """Test getting list with spaces"""
        os.environ['ITEMS'] = 'item1, item2, item3'
        config = ConfigBuilder().add_environment().build()
        
        value = config.get_list('ITEMS')
        assert value == ['item1', 'item2', 'item3']
    
    def test_get_list_with_default(self):
        """Test get_list with default"""
        config = ConfigBuilder().build()
        
        value = config.get_list('MISSING', default=['default'])
        assert value == ['default']
    
    def test_callable_config(self):
        """Test that Config can be called as a function"""
        os.environ['KEY'] = 'value'
        config = ConfigBuilder().add_environment().build()
        
        # Config should be callable
        assert config('KEY') == 'value'
        assert config('MISSING', default='default') == 'default'
    
    def test_cast_parameter(self):
        """Test using cast parameter"""
        os.environ['PORT'] = '8080'
        os.environ['DEBUG'] = 'true'
        config = ConfigBuilder().add_environment().build()
        
        port = config.get('PORT', cast=int)
        debug = config.get('DEBUG', cast=bool)
        
        assert port == 8080
        assert isinstance(port, int)
        assert debug is True
        assert isinstance(debug, bool)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
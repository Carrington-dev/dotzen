"""
tests/test_config_sources.py - Tests for configuration sources
"""

import pytest
import os
import json
import tempfile
from pathlib import Path
from dotzen.dotzen import (
    EnvironmentSource,
    DotEnvSource,
    JsonSource,
    SecretSource,
    NullSource,
    UndefinedValueError,
)


class TestEnvironmentSource:
    """Tests for EnvironmentSource"""
    
    def setup_method(self):
        """Set up test environment"""
        os.environ.clear()
    
    def test_load_all_environment_variables(self):
        """Test loading all environment variables"""
        os.environ['TEST_VAR'] = 'test_value'
        os.environ['ANOTHER_VAR'] = 'another_value'
        
        source = EnvironmentSource()
        data = source.load()
        
        assert 'TEST_VAR' in data
        assert 'ANOTHER_VAR' in data
        assert data['TEST_VAR'] == 'test_value'
        assert data['ANOTHER_VAR'] == 'another_value'
    
    def test_load_with_prefix(self):
        """Test loading environment variables with prefix"""
        os.environ['APP_DATABASE_URL'] = 'postgresql://localhost'
        os.environ['APP_SECRET_KEY'] = 'secret123'
        os.environ['OTHER_VAR'] = 'should_not_load'
        
        source = EnvironmentSource(prefix='APP_')
        data = source.load()
        
        assert 'DATABASE_URL' in data
        assert 'SECRET_KEY' in data
        assert 'OTHER_VAR' not in data
        assert data['DATABASE_URL'] == 'postgresql://localhost'
    
    def test_exists_always_true(self):
        """Test that environment source always exists"""
        source = EnvironmentSource()
        assert source.exists() is True
    
    def test_get_existing_key(self):
        """Test getting an existing key"""
        os.environ['MY_KEY'] = 'my_value'
        source = EnvironmentSource()
        
        value = source.get('MY_KEY')
        assert value == 'my_value'
    
    def test_get_with_default(self):
        """Test getting non-existent key with default"""
        source = EnvironmentSource()
        value = source.get('NON_EXISTENT', default='default_value')
        assert value == 'default_value'
    
    def test_get_without_default_raises(self):
        """Test getting non-existent key without default raises error"""
        source = EnvironmentSource()
        with pytest.raises(UndefinedValueError):
            source.get('NON_EXISTENT')


class TestDotEnvSource:
    """Tests for DotEnvSource"""
    
    def setup_method(self):
        """Create temporary .env file for testing"""
        self.temp_dir = tempfile.mkdtemp()
        self.env_file = Path(self.temp_dir) / '.env'
    
    def teardown_method(self):
        """Clean up temporary files"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_load_simple_env_file(self):
        """Test loading a simple .env file"""
        self.env_file.write_text(
            "DATABASE_URL=postgresql://localhost\n"
            "API_KEY=secret123\n"
            "PORT=5432\n"
        )
        
        source = DotEnvSource(self.env_file)
        data = source.load()
        
        assert data['DATABASE_URL'] == 'postgresql://localhost'
        assert data['API_KEY'] == 'secret123'
        assert data['PORT'] == '5432'
    
    def test_load_with_quoted_values(self):
        """Test loading values with quotes"""
        self.env_file.write_text(
            'SINGLE_QUOTED=\'single quotes\'\n'
            'DOUBLE_QUOTED="double quotes"\n'
            'NO_QUOTES=no quotes\n'
        )
        
        source = DotEnvSource(self.env_file)
        data = source.load()
        
        assert data['SINGLE_QUOTED'] == 'single quotes'
        assert data['DOUBLE_QUOTED'] == 'double quotes'
        assert data['NO_QUOTES'] == 'no quotes'
    
    def test_load_with_comments(self):
        """Test that comments are ignored"""
        self.env_file.write_text(
            "# This is a comment\n"
            "KEY1=value1\n"
            "# Another comment\n"
            "KEY2=value2\n"
        )
        
        source = DotEnvSource(self.env_file)
        data = source.load()
        
        assert 'KEY1' in data
        assert 'KEY2' in data
        assert len(data) == 2
    
    def test_load_with_empty_lines(self):
        """Test that empty lines are ignored"""
        self.env_file.write_text(
            "KEY1=value1\n"
            "\n"
            "KEY2=value2\n"
            "\n\n"
            "KEY3=value3\n"
        )
        
        source = DotEnvSource(self.env_file)
        data = source.load()
        
        assert len(data) == 3
    
    def test_load_with_equals_in_value(self):
        """Test values containing equals signs"""
        self.env_file.write_text(
            "CONNECTION_STRING=Server=localhost;Database=test\n"
        )
        
        source = DotEnvSource(self.env_file)
        data = source.load()
        
        assert data['CONNECTION_STRING'] == 'Server=localhost;Database=test'
    
    def test_load_with_spaces(self):
        """Test handling of spaces around keys and values"""
        self.env_file.write_text(
            "  KEY1  =  value1  \n"
            "KEY2=value2\n"
        )
        
        source = DotEnvSource(self.env_file)
        data = source.load()
        
        assert data['KEY1'] == 'value1'
        assert data['KEY2'] == 'value2'
    
    def test_exists_when_file_exists(self):
        """Test exists returns True when file exists"""
        self.env_file.write_text("KEY=value\n")
        source = DotEnvSource(self.env_file)
        assert source.exists() is True
    
    def test_exists_when_file_missing(self):
        """Test exists returns False when file doesn't exist"""
        source = DotEnvSource(Path(self.temp_dir) / 'missing.env')
        assert source.exists() is False
    
    def test_load_missing_file_returns_empty(self):
        """Test loading missing file returns empty dict"""
        source = DotEnvSource(Path(self.temp_dir) / 'missing.env')
        data = source.load()
        assert data == {}
    
    def test_caching(self):
        """Test that loaded data is cached"""
        self.env_file.write_text("KEY=value\n")
        source = DotEnvSource(self.env_file)
        
        data1 = source.load()
        data2 = source.load()
        
        assert data1 is data2  # Same object reference


class TestJsonSource:
    """Tests for JsonSource"""
    
    def setup_method(self):
        """Create temporary directory for test files"""
        self.temp_dir = tempfile.mkdtemp()
        self.json_file = Path(self.temp_dir) / 'config.json'
    
    def teardown_method(self):
        """Clean up temporary files"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_load_simple_json(self):
        """Test loading simple JSON configuration"""
        config = {
            "database_url": "postgresql://localhost",
            "api_key": "secret123",
            "port": "5432"
        }
        self.json_file.write_text(json.dumps(config))
        
        source = JsonSource(self.json_file)
        data = source.load()
        
        assert data['database_url'] == 'postgresql://localhost'
        assert data['api_key'] == 'secret123'
        assert data['port'] == '5432'
    
    def test_load_nested_json(self):
        """Test loading nested JSON with dot notation"""
        config = {
            "database": {
                "host": "localhost",
                "port": "5432",
                "credentials": {
                    "username": "admin",
                    "password": "secret"
                }
            },
            "api": {
                "key": "api123"
            }
        }
        self.json_file.write_text(json.dumps(config))
        
        source = JsonSource(self.json_file)
        data = source.load()
        
        assert data['database.host'] == 'localhost'
        assert data['database.port'] == '5432'
        assert data['database.credentials.username'] == 'admin'
        assert data['database.credentials.password'] == 'secret'
        assert data['api.key'] == 'api123'
    
    def test_load_mixed_types(self):
        """Test that all values are converted to strings"""
        config = {
            "string_val": "text",
            "int_val": 42,
            "float_val": 3.14,
            "bool_val": True,
            "null_val": None
        }
        self.json_file.write_text(json.dumps(config))
        
        source = JsonSource(self.json_file)
        data = source.load()
        
        assert data['string_val'] == 'text'
        assert data['int_val'] == '42'
        assert data['float_val'] == '3.14'
        assert data['bool_val'] == 'True'
        assert data['null_val'] == 'None'
    
    def test_exists_when_file_exists(self):
        """Test exists returns True when file exists"""
        self.json_file.write_text('{"key": "value"}')
        source = JsonSource(self.json_file)
        assert source.exists() is True
    
    def test_exists_when_file_missing(self):
        """Test exists returns False when file doesn't exist"""
        source = JsonSource(Path(self.temp_dir) / 'missing.json')
        assert source.exists() is False
    
    def test_load_missing_file_returns_empty(self):
        """Test loading missing file returns empty dict"""
        source = JsonSource(Path(self.temp_dir) / 'missing.json')
        data = source.load()
        assert data == {}
    
    def test_caching(self):
        """Test that loaded data is cached"""
        self.json_file.write_text('{"key": "value"}')
        source = JsonSource(self.json_file)
        
        data1 = source.load()
        data2 = source.load()
        
        assert data1 is data2


class TestSecretSource:
    """Tests for SecretSource (Docker secrets)"""
    
    def setup_method(self):
        """Create temporary secrets directory"""
        self.temp_dir = tempfile.mkdtemp()
        self.secrets_dir = Path(self.temp_dir) / 'secrets'
        self.secrets_dir.mkdir()
    
    def teardown_method(self):
        """Clean up temporary files"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_load_secrets(self):
        """Test loading secrets from directory"""
        (self.secrets_dir / 'db_password').write_text('postgres123')
        (self.secrets_dir / 'api_key').write_text('secret_api_key')
        
        source = SecretSource(self.secrets_dir)
        data = source.load()
        
        assert data['db_password'] == 'postgres123'
        assert data['api_key'] == 'secret_api_key'
    
    def test_load_secrets_strips_whitespace(self):
        """Test that secret values are stripped of whitespace"""
        (self.secrets_dir / 'token').write_text('  my_token  \n')
        
        source = SecretSource(self.secrets_dir)
        data = source.load()
        
        assert data['token'] == 'my_token'
    
    def test_ignores_subdirectories(self):
        """Test that subdirectories are ignored"""
        (self.secrets_dir / 'secret1').write_text('value1')
        subdir = self.secrets_dir / 'subdir'
        subdir.mkdir()
        (subdir / 'secret2').write_text('value2')
        
        source = SecretSource(self.secrets_dir)
        data = source.load()
        
        assert 'secret1' in data
        assert 'subdir' not in data
        assert len(data) == 1
    
    def test_exists_when_directory_exists(self):
        """Test exists returns True when directory exists"""
        source = SecretSource(self.secrets_dir)
        assert source.exists() is True
    
    def test_exists_when_directory_missing(self):
        """Test exists returns False when directory doesn't exist"""
        source = SecretSource(Path(self.temp_dir) / 'missing')
        assert source.exists() is False
    
    def test_load_missing_directory_returns_empty(self):
        """Test loading missing directory returns empty dict"""
        source = SecretSource(Path(self.temp_dir) / 'missing')
        data = source.load()
        assert data == {}
    
    def test_caching(self):
        """Test that loaded data is cached"""
        (self.secrets_dir / 'secret').write_text('value')
        source = SecretSource(self.secrets_dir)
        
        data1 = source.load()
        data2 = source.load()
        
        assert data1 is data2


class TestNullSource:
    """Tests for NullSource"""
    
    def test_load_returns_empty(self):
        """Test that load returns empty dict"""
        source = NullSource()
        data = source.load()
        assert data == {}
    
    def test_exists_returns_false(self):
        """Test that exists returns False"""
        source = NullSource()
        assert source.exists() is False
    
    def test_get_with_default(self):
        """Test getting value with default"""
        source = NullSource()
        value = source.get('key', default='default')
        assert value == 'default'
    
    def test_get_without_default_raises(self):
        """Test getting value without default raises error"""
        source = NullSource()
        with pytest.raises(UndefinedValueError):
            source.get('key')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
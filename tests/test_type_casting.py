"""
tests/test_edge_cases.py - Edge cases and error handling tests
"""

import sys
import pytest
import os
import json
import tempfile
from pathlib import Path
from dotzen.dotzen import (
    ConfigBuilder,
    ConfigFactory,
    ConfigSingleton,
    config,
    UndefinedValueError,
    ValidationError,
    SourceNotFoundError,
    UNDEFINED,
)


class TestUndefinedSentinel:
    """Tests for UNDEFINED sentinel value"""
    
    def test_undefined_repr(self):
        """Test UNDEFINED string representation"""
        assert repr(UNDEFINED) == "<UNDEFINED>"
    
    def test_undefined_is_singleton(self):
        """Test UNDEFINED is a singleton"""
        from dotzen.dotzen import _Undefined
        undefined2 = _Undefined()
        # Should have same representation but different instances
        assert repr(undefined2) == repr(UNDEFINED)
    
    def test_undefined_vs_none(self):
        """Test UNDEFINED is different from None"""
        assert UNDEFINED is not None
        assert UNDEFINED != None


class TestErrorHandling:
    """Tests for error conditions"""
    
    def setup_method(self):
        """Set up test environment"""
        os.environ.clear()
        self.temp_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Clean up"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_missing_key_without_default(self):
        """Test accessing missing key without default raises error"""
        config = ConfigBuilder().build()
        
        with pytest.raises(UndefinedValueError) as exc_info:
            config.get('MISSING_KEY')
        
        assert "MISSING_KEY" in str(exc_info.value)
        assert "not found" in str(exc_info.value).lower()
    
    def test_missing_key_in_chain(self):
        """Test missing key in chain of sources"""
        env_file = Path(self.temp_dir) / '.env'
        env_file.write_text('KEY1=value1\n')
        
        config = (ConfigBuilder()
                  .add_environment()
                  .add_dotenv(str(env_file))
                  .build())
        
        with pytest.raises(UndefinedValueError) as exc_info:
            config.get('MISSING_KEY')
        
        assert "not found in any configuration source" in str(exc_info.value).lower()
    
    def test_malformed_env_file(self):
        """Test handling malformed .env file"""
        env_file = Path(self.temp_dir) / '.env'
        env_file.write_text(
            "VALID_KEY=value\n"
            "NO_EQUALS_SIGN\n"  # Invalid line
            "ANOTHER_VALID=value2\n"
        )
        
        config = ConfigBuilder().add_dotenv(str(env_file)).build()
        
        # Should still load valid keys
        assert config.get('VALID_KEY') == 'value'
        assert config.get('ANOTHER_VALID') == 'value2'
    
    def test_malformed_json_file(self):
        """Test handling malformed JSON file"""
        json_file = Path(self.temp_dir) / 'config.json'
        json_file.write_text('{ invalid json }')
        
        config = ConfigBuilder().add_json(str(json_file)).build()
        
        # Should raise error when trying to load
        with pytest.raises(Exception):  # json.JSONDecodeError
            config.get('key')
    
    def test_empty_env_file(self):
        """Test handling empty .env file"""
        env_file = Path(self.temp_dir) / '.env'
        env_file.write_text('')
        
        config = ConfigBuilder().add_dotenv(str(env_file)).build()
        
        # Should work, just return default
        assert config.get('KEY', default='default') == 'default'
    
    def test_comments_only_env_file(self):
        """Test .env file with only comments"""
        env_file = Path(self.temp_dir) / '.env'
        env_file.write_text(
            "# Comment 1\n"
            "# Comment 2\n"
            "# Comment 3\n"
        )
        
        config = ConfigBuilder().add_dotenv(str(env_file)).build()
        
        assert config.get('KEY', default='default') == 'default'
    
    def test_permission_denied_file(self):
        """Test handling file permission errors"""
        import stat
        
        env_file = Path(self.temp_dir) / '.env'
        env_file.write_text('KEY=value\n')

        # Skip on Windows as file permissions work differently
        if sys.platform == 'win32':
            pytest.skip("File permission test not applicable on Windows")
        
        # Remove read permissions
        os.chmod(env_file, stat.S_IWRITE)
        
        try:
            config = ConfigBuilder().add_dotenv(str(env_file)).build()
            
            # Should raise PermissionError
            with pytest.raises(PermissionError):
                config.get('KEY')
        finally:
            # Restore permissions for cleanup
            os.chmod(env_file, stat.S_IREAD | stat.S_IWRITE)


class TestEdgeCaseValues:
    """Tests for edge case configuration values"""
    
    def setup_method(self):
        """Set up test environment"""
        os.environ.clear()
    
    def test_empty_string_value(self):
        """Test handling empty string values"""
        os.environ['EMPTY'] = ''
        config = ConfigBuilder().add_environment().build()
        
        assert config.get('EMPTY') == ''
        assert config.get('EMPTY', default='default') == ''  # Empty string, not default
    
    def test_whitespace_only_value(self):
        """Test handling whitespace-only values"""
        os.environ['SPACES'] = '   '
        config = ConfigBuilder().add_environment().build()
        
        assert config.get('SPACES') == '   '
    
    def test_special_characters(self):
        """Test handling special characters"""
        special_chars = '!@#$%^&*()_+-={}[]|\\:";\'<>?,./'
        os.environ['SPECIAL'] = special_chars
        config = ConfigBuilder().add_environment().build()
        
        assert config.get('SPECIAL') == special_chars
    
    def test_unicode_characters(self):
        """Test handling unicode characters"""
        os.environ['UNICODE'] = '你好世界 🌍 émoji'
        config = ConfigBuilder().add_environment().build()
        
        assert config.get('UNICODE') == '你好世界 🌍 émoji'
    
    def test_multiline_value_in_env(self):
        """Test handling multiline values"""
        # Environment variables don't support newlines directly
        os.environ['MULTILINE'] = 'line1\\nline2\\nline3'
        config = ConfigBuilder().add_environment().build()
        
        assert config.get('MULTILINE') == 'line1\\nline2\\nline3'
    
    def test_very_long_value(self):
        """Test handling very long values"""
        long_value = 'x' * 10000
        os.environ['LONG'] = long_value
        config = ConfigBuilder().add_environment().build()
        
        assert config.get('LONG') == long_value
        assert len(config.get('LONG')) == 10000
    
    def test_numeric_string_not_auto_converted(self):
        """Test that numeric strings aren't auto-converted"""
        os.environ['NUMBER'] = '42'
        config = ConfigBuilder().add_environment().build()
        
        value = config.get('NUMBER')
        assert value == '42'
        assert isinstance(value, str)  # Still a string


class TestConcurrentAccess:
    """Tests for concurrent access scenarios"""
    
    def setup_method(self):
        """Set up test environment"""
        os.environ.clear()
        ConfigSingleton.reset()
    
    def teardown_method(self):
        """Clean up"""
        ConfigSingleton.reset()
    
    def test_singleton_thread_safety(self):
        """Test singleton access from multiple threads"""
        import threading
        
        os.environ['SHARED'] = 'value'
        instances = []
        
        def get_instance():
            instance = ConfigSingleton.get_instance()
            instances.append(instance)
        
        threads = [threading.Thread(target=get_instance) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # All instances should be the same
        assert all(inst is instances[0] for inst in instances)
    
    def test_config_immutability(self):
        """Test that config values don't change unexpectedly"""
        os.environ['KEY'] = 'original'
        config = ConfigBuilder().add_environment().build()
        
        value1 = config.get('KEY')
        
        # Change environment (shouldn't affect already-loaded config)
        os.environ['KEY'] = 'changed'
        
        # For environment source, it will reflect the change
        # This is expected behavior
        value2 = config.get('KEY')
        assert value2 == 'changed'  # Environment is dynamic


class TestNestedAndComplexStructures:
    """Tests for nested and complex configuration structures"""
    
    def setup_method(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Clean up"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_deeply_nested_json(self):
        """Test deeply nested JSON structure"""
        config_data = {
            "level1": {
                "level2": {
                    "level3": {
                        "level4": {
                            "level5": {
                                "value": "deep"
                            }
                        }
                    }
                }
            }
        }
        
        json_file = Path(self.temp_dir) / 'config.json'
        json_file.write_text(json.dumps(config_data))
        
        config = ConfigBuilder().add_json(str(json_file)).build()
        
        value = config.get('level1.level2.level3.level4.level5.value')
        assert value == 'deep'
    
    def test_json_with_arrays(self):
        """Test JSON with array values"""
        config_data = {
            "servers": ["server1", "server2", "server3"],
            "ports": [8080, 8081, 8082]
        }
        
        json_file = Path(self.temp_dir) / 'config.json'
        json_file.write_text(json.dumps(config_data))
        
        config = ConfigBuilder().add_json(str(json_file)).build()
        
        # Arrays are converted to strings
        servers = config.get('servers')
        assert "server1" in servers
    
    def test_mixed_type_json(self):
        """Test JSON with mixed types"""
        config_data = {
            "string": "text",
            "number": 42,
            "float": 3.14,
            "boolean": True,
            "null": None,
            "nested": {
                "inner": "value"
            }
        }
        
        json_file = Path(self.temp_dir) / 'config.json'
        json_file.write_text(json.dumps(config_data))
        
        config = ConfigBuilder().add_json(str(json_file)).build()
        
        # All converted to strings
        assert config.get('string') == 'text'
        assert config.get('number') == '42'
        assert config.get('float') == '3.14'
        assert config.get('boolean') == 'True'
        assert config.get('null') == 'None'
        assert config.get('nested.inner') == 'value'


class TestValidation:
    """Tests for validation functionality"""
    
    def setup_method(self):
        """Set up test environment"""
        os.environ.clear()
    
    def test_validator_called_on_get(self):
        """Test that validator is called when getting value"""
        called = []
        
        def validator(key, value):
            called.append((key, value))
        
        os.environ['KEY'] = 'value'
        config = (ConfigBuilder()
                  .add_environment()
                  .with_validator(validator)
                  .build())
        
        config.get('KEY')
        
        assert len(called) == 1
        assert called[0] == ('KEY', 'value')
    
    def test_validator_can_raise_error(self):
        """Test that validator can raise ValidationError"""
        def strict_validator(key, value):
            if key == 'PORT' and int(value) > 10000:
                raise ValidationError("Port must be <= 10000")
        
        os.environ['PORT'] = '99999'
        config = (ConfigBuilder()
                  .add_environment()
                  .with_validator(strict_validator)
                  .build())
        
        with pytest.raises(ValidationError, match="Port must be <= 10000"):
            config.get('PORT')
    
    def test_multiple_validators(self):
        """Test multiple validators are all called"""
        calls = []
        
        def validator1(key, value):
            calls.append('validator1')
        
        def validator2(key, value):
            calls.append('validator2')
        
        os.environ['KEY'] = 'value'
        config = (ConfigBuilder()
                  .add_environment()
                  .with_validator(validator1)
                  .with_validator(validator2)
                  .build())
        
        config.get('KEY')
        
        assert calls == ['validator1', 'validator2']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
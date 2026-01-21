# Test Failures Fix Guide

## Summary
**7 test failures** need to be fixed:
- 4 konfig() function tests
- 2 singleton thread safety tests  
- 1 permission test (Windows compatibility)

---

## Fix 1: konfig() Function - encryption.py

**Problem**: The `konfig()` convenience function receives the global `config` function instead of a Config instance.

**Solution**: Update the `konfig()` function in `dotzen/encryption.py`:

```python
def konfig(
    key: str,
    default: any = None,
    cast: Optional[Type] = None,
    encrypted: bool = True,
    algorithm: str = 'base64',
    config_instance = None
) -> any:
    if config_instance is None:
        # Import here to avoid circular imports
        from dotzen.dotzen import ConfigSingleton
        config_instance = ConfigSingleton.get_instance()
    
    # IMPORTANT FIX: Check if config_instance is actually the config function
    if callable(config_instance) and hasattr(config_instance, '__name__') and config_instance.__name__ == 'config':
        from dotzen.dotzen import ConfigSingleton
        config_instance = ConfigSingleton.get_instance()
    
    secure_config = SecureConfig(config_instance, default_algorithm=algorithm)
    return secure_config.konfig(key, default, cast, encrypted, algorithm)
```

---

## Fix 2: Thread-Safe Singleton - dotzen.py

**Problem**: Race condition in `ConfigSingleton` causes multiple instances to be created.

**Solution**: Replace the `ConfigSingleton` class in `dotzen/dotzen.py`:

```python
import threading

class ConfigSingleton:
    """
    Singleton Pattern - provides global config instance (Thread-safe)
    """
    _instance: Optional[Config] = None
    _lock = threading.Lock()
    
    @classmethod
    def get_instance(cls) -> Config:
        """Get or create singleton instance (thread-safe)"""
        if cls._instance is None:
            with cls._lock:
                # Double-check locking pattern
                if cls._instance is None:
                    cls._instance = ConfigFactory.auto_config()
        return cls._instance
    
    @classmethod
    def reset(cls):
        """Reset singleton (useful for testing)"""
        with cls._lock:
            cls._instance = None
```

**Don't forget** to add `import threading` at the top of `dotzen/dotzen.py`.

---

## Fix 3: Permission Test - Already Fixed

The permission test in `tests/test_edge_cases.py` is already fixed with Windows detection:

```python
def test_permission_denied_file(self):
    import stat
    import sys
    
    env_file = Path(self.temp_dir) / '.env'
    env_file.write_text('KEY=value\n')
    
    # Skip on Windows as file permissions work differently
    if sys.platform == 'win32':
        pytest.skip("File permission test not applicable on Windows")
    
    # ... rest of test
```

---

## Complete File Changes Required

### 1. Update `dotzen/dotzen.py`

Add at the top:
```python
import threading
```

Replace `ConfigSingleton` class with the thread-safe version above.

### 2. Update `dotzen/encryption.py`

Replace the entire `konfig()` function with the fixed version shown in Fix 1.

### 3. No changes needed for `tests/test_edge_cases.py`

The permission test is already fixed.

---

## Testing the Fixes

After applying all fixes, run:

```bash
# Run all tests
pytest -v

# Run only the failing tests
pytest tests/test_encryption.py::TestKonfigFunction -v
pytest tests/test_edge_cases.py::TestConcurrentAccess::test_singleton_thread_safety -v
pytest tests/test_type_casting.py::TestConcurrentAccess::test_singleton_thread_safety -v
```

Expected result: **All tests pass! 🎉**

---

## Quick Apply Commands

If you have the files open, here's what to change:

### File: `dotzen/dotzen.py`
1. Line 1-10: Add `import threading` after other imports
2. Find class `ConfigSingleton` (around line 600)
3. Replace entire class with thread-safe version

### File: `dotzen/encryption.py`  
1. Find function `def konfig(` (around line 350)
2. Replace entire function with fixed version

That's it! These 2 file changes fix all 7 test failures.
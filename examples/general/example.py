# ============================================================================
# EXAMPLE USAGE
# ============================================================================

import os
from dotzen.dotzen import ConfigBuilder, ConfigFactory, config


if __name__ == "__main__":
    # Example 1: Using the builder pattern
    print("=== Example 1: Builder Pattern ===")
    config1 = (ConfigBuilder()
               .add_environment()
               .add_dotenv('.env')
               .build())
    
    # Example 2: Using the factory pattern
    print("\n=== Example 2: Factory Pattern ===")
    config2 = ConfigFactory.auto_config()
    
    # Example 3: Using convenience function
    print("\n=== Example 3: Convenience Function ===")
    try:
        debug_mode = config('DEBUG', default='false', cast=bool)
        print(f"Debug mode: {debug_mode}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 4: Type casting
    print("\n=== Example 4: Type Casting ===")
    os.environ['PORT'] = '8080'
    os.environ['ALLOWED_HOSTS'] = 'localhost,127.0.0.1,example.com'
    
    port = config('PORT', cast=int)
    hosts = config('ALLOWED_HOSTS', cast=list)
    
    print(f"Port: {port} (type: {type(port).__name__})")
    print(f"Allowed hosts: {hosts} (type: {type(hosts).__name__})")
    
    print("\n=== Design Patterns Implemented ===")
    print("✓ Strategy Pattern - ConfigSource hierarchy")
    print("✓ Chain of Responsibility - ConfigChain")
    print("✓ Builder Pattern - ConfigBuilder")
    print("✓ Factory Pattern - ConfigFactory")
    print("✓ Singleton Pattern - ConfigSingleton")
    print("✓ Facade Pattern - Config class")
    print("✓ Null Object Pattern - NullSource")
    print("✓ Sentinel Pattern - UNDEFINED marker")
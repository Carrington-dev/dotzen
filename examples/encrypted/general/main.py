
from dotzen import EncryptionManager


if __name__ == "__main__":
    # Demo usage
    print("=== DotZen Encryption Demo ===\n")
    
    # Base64 encryption
    print("1. Base64 Encryption:")
    original = "carrington"
    encrypted = EncryptionManager.encrypt(original, 'base64')
    decrypted = EncryptionManager.decrypt(encrypted, 'base64')
    print(f"Original:  {original}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print()
    
    # MD5 hashing (one-way)
    print("2. MD5 Hashing (one-way):")
    hashed = EncryptionManager.encrypt("password123", 'md5')
    print(f"Hashed: {hashed}")
    print()
    
    # SHA256 hashing (one-way)
    print("3. SHA256 Hashing (one-way):")
    hashed = EncryptionManager.encrypt("password123", 'sha256')
    print(f"Hashed: {hashed}")
    print()
    
    # Encrypt for .env file
    print("4. Encrypt for .env file:")
    # env_value = encrypt_for_env("my-super-secret-api-key")
    # print(f"Add to .env: API_KEY={env_value}")
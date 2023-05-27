from cryptography.fernet import Fernet

def generate_key():
    """
    Generate a random encryption key.
    """
    return Fernet.generate_key()

def encrypt_password(key, password):
    """
    Encrypt the password using the provided encryption key.
    """
    cipher_suite = Fernet(key)
    encrypted_password = cipher_suite.encrypt(password.encode())
    return encrypted_password

def decrypt_password(key, encrypted_password):
    """
    Decrypt the encrypted password using the provided encryption key.
    """
    cipher_suite = Fernet(key)
    decrypted_password = cipher_suite.decrypt(encrypted_password)
    return decrypted_password.decode()

# Generate a random encryption key
encryption_key = generate_key()

# Password to encrypt and decrypt
password = "mysecretpassword"

# Encrypt the password
encrypted = encrypt_password(encryption_key, password)
print("Encrypted password:", encrypted)

# Decrypt the password
decrypted = decrypt_password(encryption_key, encrypted)
print("Decrypted password:", decrypted)

print(str(encryption_key))
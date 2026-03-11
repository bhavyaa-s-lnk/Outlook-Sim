import hashlib
import os

class SecurityManager:
    """
    Handles security-related utilities: Hashing, Encryption, and Signatures.
    
    Concept 1: Password Hashing
    Never store passwords in plain text! If a database is leaked, hackers get everything.
    Hashing is a ONE-WAY function. You can't turn a hash back into a password.
    Salting adds random data to the password before hashing to prevent 'Rainbow Table' attacks.
    """

    @staticmethod
    def hash_password(password):
        """
        Hashes a password with a salt.
        Returns: salt + hash string
        """
        # A salt is random data added to the password to make its hash unique
        salt = os.urandom(16) # 16 bytes of random data
        
        # SHA-256 is a common cryptographic hash algorithm
        hash_obj = hashlib.pbkdf2_hmac(
            'sha256', 
            password.encode('utf-8'), 
            salt, 
            100000 # Iterations - makes it slower for hackers to guess
        )
        # We store the salt with the hash so we can verify it later
        return salt.hex() + ":" + hash_obj.hex()

    @staticmethod
    def verify_password(stored_password, provided_password):
        """
        Verifies a provided password against a stored hash.
        """
        try:
            salt_hex, hash_hex = stored_password.split(":")
            salt = bytes.fromhex(salt_hex)
            
            # Re-hash the provided password using the same salt
            new_hash = hashlib.pbkdf2_hmac(
                'sha256', 
                provided_password.encode('utf-8'), 
                salt, 
                100000
            )
            return new_hash.hex() == hash_hex
        except Exception:
            return False

    # Concept 2: Key-based Encryption (Two-way)
    # Unlike hashing, encryption allows you to get the original data back IF you have the secret key.
    # We will use a Vigenère Cipher: It uses a keyword to shift letters by different amounts.
    @staticmethod
    def vigenere_encrypt(text, key):
        """Encrypts text using a Vigenère cipher and a key."""
        encrypted = []
        key = key.lower()
        key_index = 0
        for char in text:
            if char.isalpha():
                shift = ord(key[key_index % len(key)]) - ord('a')
                base = ord('A') if char.isupper() else ord('a')
                encrypted.append(chr((ord(char) - base + shift) % 26 + base))
                key_index += 1
            else:
                encrypted.append(char)
        return "".join(encrypted)

    @staticmethod
    def vigenere_decrypt(text, key):
        """Decrypts text using a Vigenère cipher and a key."""
        decrypted = []
        key = key.lower()
        key_index = 0
        for char in text:
            if char.isalpha():
                shift = ord(key[key_index % len(key)]) - ord('a')
                base = ord('A') if char.isupper() else ord('a')
                decrypted.append(chr((ord(char) - base - shift) % 26 + base))
                key_index += 1
            else:
                decrypted.append(char)
        return "".join(decrypted)

    # Concept 3: Digital Signatures (Integrity)
    # Ensures the message wasn't tampered with.
    @staticmethod
    def sign_message(message, secret_key):
        """Creates a simple signature (HMAC-like) for a message."""
        combined = message + secret_key
        return hashlib.sha256(combined.encode()).hexdigest()[:10]

    @staticmethod
    def verify_signature(message, signature, secret_key):
        """Verifies if the signature matches the message."""
        expected = SecurityManager.sign_message(message, secret_key)
        return expected == signature

if __name__ == "__main__":
    # Quick test for the concepts
    sm = SecurityManager()
    p = "SuperSecret123"
    hashed = sm.hash_password(p)
    print(f"Password: {p}")
    print(f"Hashed: {hashed}")
    print(f"Verify Correct: {sm.verify_password(hashed, p)}")
    print(f"Verify Wrong: {sm.verify_password(hashed, 'WrongPass')}")

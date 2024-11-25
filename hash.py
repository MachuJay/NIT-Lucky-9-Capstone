import hashlib

# Function to hash a password using MD5
def hash_password_md5(password: str) -> str:
    # Encode the password to bytes, then hash it
    hashed = hashlib.md5(password.encode()).hexdigest()
    return hashed

# Example usage
if __name__ == "__main__":
    # Input password
    plain_password = "22"

    # Hash the password
    hashed_password = hash_password_md5(plain_password)
    print(f"MD5 Hashed password: {hashed_password}")
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
import hashlib
import os
import uuid

def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    return public_key, private_key

def sign_data(data, private_key):
    message_digest = hashlib.sha256(data.encode()).hexdigest()

    concatenated_data = data + message_digest

    signature = private_key.sign(
        concatenated_data.encode('utf-8'),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    file_name = f"{str(uuid.uuid4().fields[-1])[:8]}.bin"
    with open(file_name, 'wb') as signature_file:
        signature_file.write(concatenated_data.encode('utf-8') + signature)
    print(f"Signature saved to {file_name}")

def verify_data(signature_file_path, public_key):
    try:
        with open(signature_file_path, 'rb') as signature_file:
            content = signature_file.read()

        key_size = 2048 // 8  # For a 2048-bit key, the signature size will be 256 bytes
        concatenated_data = content[:-key_size]
        digest = content[-key_size:]

        public_key.verify(
            digest,
            concatenated_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        print("Verification successful: The signature is valid.")
        
    except Exception as e:
        print(f"Verification failed")

if __name__ == "__main__":
    public_key, private_key = generate_keys()

    while True:
        print("\nMenu:")
        print("1. Sign Data")
        print("2. Verify Data")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            message = input("Enter the message to sign: ")
            sign_data(message, private_key)

        elif choice == '2':
            signature_file_path = input("Enter the path of the signature file: ")
            if not os.path.exists(signature_file_path):
                print("File does not exist.")
                continue
            verify_data(signature_file_path, public_key)

        elif choice == '3':
            print("Exiting.")
            break

        else:
            print("Invalid choice.")

Secure File Sharing System – Security Overview
1. Project Summary

This project implements a secure file sharing system where users can safely upload and download files. The focus is on data confidentiality, integrity, and secure handling of encryption keys. It is built with Python Flask and uses AES encryption to protect file contents both in storage and during transfer.

2. Core Features

User Authentication: Single user login system to access the file portal. Passwords are securely hashed using Werkzeug.

File Upload/Download: Users can upload files, which are stored in an encrypted form, and later download the decrypted files.

AES Encryption: Files are encrypted using AES-GCM, which provides both confidentiality and integrity verification.

Key Management: A master passphrase stored in .env is used to derive encryption keys. This ensures the keys are never hardcoded in the codebase.

Secure File Storage: Encrypted files include associated metadata (nonce, tag) for proper decryption.

3. Security Approach
3.1 AES Encryption

Mode: AES-GCM (Galois/Counter Mode)

Purpose: Provides confidentiality (encrypts file content) and integrity (verifies content during decryption).

File Metadata: Each file stores a unique nonce and authentication tag along with the encrypted content.

3.2 Key Management

Master Passphrase: Defined in a .env file (e.g., MASTER_PASSPHRASE).

Derivation: The master passphrase is used to generate a consistent encryption key for files.

Environment Variables: Keeps sensitive information out of the source code, reducing the risk of exposure in public repositories.

3.3 Password Security

Hashing: User passwords are hashed using Werkzeug’s generate_password_hash.

Verification: Login checks use check_password_hash to compare the hashed password, never storing plaintext passwords.

3.4 File Integrity

GCM Tag Verification: During decryption, the GCM tag ensures that files have not been tampered with. Any modification or corruption will raise an error.

4. Usage Instructions

Clone the repository:

git clone https://github.com/YourUsername/FUTURE_CS_03.git
cd FUTURE_CS_03


Install dependencies:

python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
pip install -r requirements.txt


Create a .env file in the project root:

MASTER_PASSPHRASE=your_secret_passphrase
APP_USER=admin
APP_PASS=strongpassword


Initialize the database and create a default user.

Run the app:

python run.py


Access the system at http://127.0.0.1:5000, log in, upload files, and download securely.

5. Future Improvements

Multi-user support: Allow multiple accounts with isolated file storage.

Advanced key management: Use per-user or per-file encryption keys.

Enhanced logging & auditing: Track uploads, downloads, and access attempts.

File size & type restrictions: Prevent uploading unsafe or extremely large files.

6. Learning Outcomes

Implementing AES encryption in a real-world web app.

Secure handling of passwords and environment secrets.

Web development with Flask for secure file operations.

Practical understanding of encryption, authentication, and key management.

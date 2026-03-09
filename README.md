# secure-valut

 # PROJECT REPORT: AES-256 SECURE FILE VAULT

#  Muhammed Aslam

#  Cyber Security

# Date: March 2026

________________________________________

##  1. PROJECT OVERVIEW

The Secure Vault is designed to provide robust confidentiality and integrity for local files. this project implements Authenticated Encryption to ensure that sensitive data remains encrypted

## 2. CORE SPECIFICATIONS

•	Encryption Algorithm: AES-256 

•	Mode of Operation: CBC with Fernet

•	Key Derivation: PBKDF2 (Password-Based Key Derivation Function 2)

•	Hashing: SHA-256 for integrity verification

•	Interface: PyQt5 Modern Dark-Theme GUI

________________________________________

## 3. TECHNICAL ARCHITECTURE

### 3.1 Key Stretching with PBKDF2

A common vulnerability in encryption tools is the use of weak user passwords. This project mitigates this by "stretching" the password:

1.	Salt: A unique 16-byte random value is generated for every file

2.	Iterations: The password and salt pass through 480,000 iterations of SHA-256

3.	Resistance: This makes "brute-force" and "dictionary attacks"


### 3.2 The Encryption Pipeline
The application bundles the following components into a single .enc file:

•	Salt (16 bytes): Stored in plaintext at the beginning of the file to allow key re-derivation.

•	Ciphertext: The AES-encrypted data.

•	HMAC/Integrity Tag: A signature that ensures the file hasn't been modified.

________________________________________

## 4. SECURITY FEATURES & DEFENSES
________________________________________

AES-256 bit Key: Protection against brute-force decryption

Unique Salting:   Prevents "Rainbow Table" attacks; same password yields different ciphertext

SHA-256 Integrity : Detects "Bit-Flipping" attacks; if 1 bit changes, decryption is denied

Secure Nemory : Passwords are encoded to bytes and cleared from variables after use


## 5. SYSTEM IMPLEMENTATION

1.	Backend Logic: Developed the SecureVault class using the cryptography library

  
2.	Integrity Layer: Integrated SHA-256 hashing to verify file state post-decryption
  

4.	GUI Design: Created a professional "Cyber-Vault" interface using PyQt5 and QSS (Qt Style Sheets)


________________________________________


## 6. HOW TO OPERATE

### 1.	Initialize Environment:

```Bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install required packages :

```Bash
pip install cryptography PyQt5
```

### 3.Run Application:
   ```
bash 
   python3 secure.py
```

### 4.	Encryption: Select a file, enter a Master Password, and click Encrypt.
### 5.	Decryption: Select the .enc file, enter the original Master Password, and click Decrypt.
________________________________________
## 7. CONCLUSION
The project successfully demonstrates a professional implementation of the CIA Triad (Confidentiality, Integrity, and Availability). By combining AES-256 with PBKDF2 key derivation and a modern GUI, the tool provides a reliable, user-friendly security solution for sensitive data storage on Kali Linux.

# 📧 Secure Outlook Simulator (OutlookSim)

### 🏛 University Coursework: COMP1811 Outlook Simulator

A high-security Python-based email simulator designed to demonstrate modern cybersecurity principles including **Cryptographic Hashing**, **Two-Way Encryption**, **Digital Signatures**, and **Role-Based Access Control (RBAC)**.

---

## 🌍 Real-World Relevance & Impact

In an era of increasing data breaches and phishing attacks, understanding the underlying security of email systems is critical. This project isn't just a simulator; it's a demonstration of how real-world enterprise systems protect sensitive data:

1. **Password Protection:** Demonstrates how "Salting" and "Iterative Hashing" (PBKDF2) prevent hackers from reading passwords even if a database is compromised.
2. **Data Integrity:** Shows how Digital Signatures detect if a message has been tampered with during transit.
3. **Privacy:** Implements two-way encryption to ensure only authorized recipients can read sensitive content.
4. **Access Control:** Simulates enterprise environments where different users (Admin vs. Regular User) have different permissions, preventing unauthorized data access.

---

## 🔐 Key Cybersecurity Features

### 1. Password Hashing (SHA-256 + Salt)
- Uses `PBKDF2_HMAC` with `SHA-256`.
- Implements unique **Salts** for every user to thwart Rainbow Table attacks.
- High iteration counts to significantly increase the cost of brute-force attacks.

### 2. Digital Signatures (Integrity)
- Every message can be signed using a secret key.
- The system verifies the signature upon receipt to ensure **Non-repudiation** and **Integrity**.

### 3. Vigenère Cipher (Encryption)
- Demonstrates polyalphabetic substitution encryption for sensitive (`Confidential`) emails.
- Allows secure communication between parties sharing a keyword.

### 4. Role-Based Access Control (RBAC)
- Filtering logic ensures that `Confidential` tagged emails are only visible to `Admin` users or intended recipients.

### 5. Input Sanitization & Spam Defense
- **Sanitization:** Strips malicious characters from user input to prevent injection attacks.
- **Heuristic Spam Check:** Automatically identifies potential phishing or spam based on sender patterns and content.

---

## 🛠 Project Structure

- `Interpreter.py`: The main CLI application loop with command sanitization.
- `SecurityManager.py`: The core security engine (Hashing, Encryption, Signatures).
- `MailboxAgent.py`: Handles mailbox logic, RBAC, and spam detection.
- `Mail.py`, `Personal.py`, `Confidential.py`: Object-oriented representation of different email types.

---

## 🚀 Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/bhavyaa-s-lnk/Outlook-Sim.git
   ```
2. **Run the simulator:**
   ```bash
   python Interpreter.py
   ```

---

*Developed as part of the **COMP1811** university curriculum. This version has been enhanced and professionally documented to serve as a portfolio demonstration of secure software engineering principles.*

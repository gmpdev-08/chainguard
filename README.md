Markdown
# 🛡️ ChainGuard

**Digital Evidence Integrity & Chain of Custody Utility**

---

## 📌 Overview

**ChainGuard** is a lightweight, Python-based Digital Forensics and Incident Response (DFIR) utility designed to ensure the cryptographic integrity of digital evidence and maintain strict **Chain of Custody** standards. 

In forensic investigations, proving that an evidence file has not been altered or tampered with since acquisition is critical. ChainGuard calculates multi-algorithm cryptographic hashes, automatically generates standardized JSON custody logs, and provides integrity verification capabilities.

---

## 🚀 Key Features

- **Multi-Algorithm Hashing:** Computes **MD5**, **SHA-1**, and **SHA-256** hashes simultaneously using memory-efficient block reading (ideal for large forensic images or files).
- **Chain of Custody Generation:** Automatically structures a metadata report (including UTC timestamps, examiner details, and file size) exported as an immutable JSON log.
- **Evidence Verification:** Compares current file hashes against original custody records to instantly detect any potential tampering or data corruption.
- **Pure Python Standard Library:** Zero external dependencies required, ensuring it can run out-of-the-box in restricted forensic environments.

---

## 🛠️ Project Structure

```text
chainguard/
├── src/
│   └── chainguard.py    # Main script containing hashing, custody, and verification logic
├── LICENSE              # MIT Open Source License
└── README.md            # Project Documentation
⚙️ How to Use
Clone the repository:

Bash
git clone [https://github.com/gmpdev-08/chainguard.git](https://github.com/gmpdev-08/chainguard.git)
cd chainguard
Run the tool:

Bash
python src/chainguard.py
Choose an option from the interactive CLI menu:

Option 1: Create a Chain of Custody record by providing the path to the evidence file and the examiner's name. It will output a .json custody log.

Option 2: Verify evidence integrity by matching a current file against its original custody JSON record.

👨‍💻 Author
Developed by Guilherme Pedro (gmpdev-08)

Aspiring Digital Forensics & DFIR Specialist | Software Engineering Student @ ISEP

📄 License
This project is licensed under the terms of the MIT License. See the LICENSE file for details.
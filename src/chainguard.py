import hashlib
import json
import os
from datetime import datetime

def calculate_hashes(file_path):
    """Calculates multiple cryptographic hashes of a file to ensure forensic integrity."""
    sha256_hash = hashlib.sha256()
    sha1_hash = hashlib.sha1()
    md5_hash = hashlib.md5()
    
    file_size = os.path.getsize(file_path)
    
    # Read file in blocks to optimize memory usage (essential for large forensic images)
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
            sha1_hash.update(byte_block)
            md5_hash.update(byte_block)
            
    return {
        "file_name": os.path.basename(file_path),
        "file_size_bytes": file_size,
        "md5": md5_hash.hexdigest(),
        "sha1": sha1_hash.hexdigest(),
        "sha256": sha256_hash.hexdigest()
    }

def create_custody_record(file_path, examiner_name):
    """Generates a structured chain of custody record with a precise timestamp."""
    if not os.path.exists(file_path):
        print(f"[!] Error: The file '{file_path}' was not found.")
        return None
        
    print(f"[*] Processing evidence and calculating cryptographic hashes...")
    file_hashes = calculate_hashes(file_path)
    
    record = {
        "case_metadata": {
            "examiner": examiner_name,
            "timestamp_utc": datetime.utcnow().isoformat() + "Z",
            "tool_name": "ChainGuard DFIR Utility",
            "version": "1.0"
        },
        "evidence_details": file_hashes
    }
    
    # Save the custody record into a structured JSON file
    output_filename = f"custody_{file_hashes['sha256'][:8]}.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=4)
        
    print(f"[+] Success! Chain of custody record generated: {output_filename}")
    return record

if __name__ == "__main__":
    print("=== ChainGuard - Digital Evidence Integrity Utility ===")
    target_file = input("Enter path to evidence file: ").strip()
    examiner = input("Forensic Examiner Name: ").strip()
    
    if target_file and examiner:
        create_custody_record(target_file, examiner)
    else:
        print("[!] Please fill in all required fields correctly.")
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

def verify_evidence(file_path, custody_json_path):
    """Verifies if a current file matches the cryptographic hashes stored in its custody record."""
    if not os.path.exists(file_path) or not os.path.exists(custody_json_path):
        print(f"[!] Error: File or custody JSON path not found.")
        return
        
    print(f"[*] Loading custody record: {custody_json_path}")
    with open(custody_json_path, "r", encoding="utf-8") as f:
        custody_data = json.load(f)
        
    stored_hashes = custody_data["evidence_details"]
    
    print(f"[*] Recalculating current hashes for: {file_path}")
    current_hashes = calculate_hashes(file_path)
    
    print("\n--- INTEGRITY VERIFICATION REPORT ---")
    match = True
    
    for algo in ["md5", "sha1", "sha256"]:
        stored_val = stored_hashes[algo]
        current_val = current_hashes[algo]
        is_equal = (stored_val == current_val)
        status = "MATCH [VALID]" if is_equal else "MISMATCH [ALERTS: TAMPERED OR MODIFIED]"
        print(f"[{algo.upper()}]")
        print(f"  Stored:  {stored_val}")
        print(f"  Current: {current_val}")
        print(f"  Status:  {status}\n")
        
        if not is_equal:
            match = False
            
    if match:
        print("[+] VERIFICATION SUCCESSFUL: The evidence integrity is intact. No tampering detected.")
    else:
        print("[!] ALERT: Evidence integrity failure! Hashes do not match. Potential data tampering.")

if __name__ == "__main__":
    print("=== ChainGuard - Digital Evidence Integrity Utility ===")
    print("1. Create Chain of Custody Record")
    print("2. Verify Evidence Integrity")
    choice = input("Select an option (1 or 2): ").strip()
    
    if choice == "1":
        target_file = input("Enter path to evidence file: ").strip()
        examiner = input("Forensic Examiner Name: ").strip()
        if target_file and examiner:
            create_custody_record(target_file, examiner)
        else:
            print("[!] Please fill in all required fields correctly.")
            
    elif choice == "2":
        target_file = input("Enter path to the current file to check: ").strip()
        custody_json = input("Enter path to the custody JSON record file: ").strip()
        if target_file and custody_json:
            verify_evidence(target_file, custody_json)
        else:
            print("[!] Please fill in all required fields correctly.")
    else:
        print("[!] Invalid option.")
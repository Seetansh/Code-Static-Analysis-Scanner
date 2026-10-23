import os
import re
import json

TARGET_DIR = "target_repo"

def scan_for_secrets(filepath):
    violations = []
    # Regex patterns for common secrets
    secret_patterns = [
        r"sk_live_[a-zA-Z0-9]{24}",
        r"(password|secret)\s*=\s*['\"].+['\"]"
    ]
    
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
    for line_num, line in enumerate(lines, 1):
        for pattern in secret_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                violations.append({
                    "rule": "SEC-01",
                    "file": filepath,
                    "line": line_num,
                    "message": "CRITICAL: Hardcoded secret detected."
                })
    return violations

def run_engine():
    all_violations = []
    
    # 1. Walk the directory
    for root, _, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                
                # 2. Run the security scan on each file
                file_violations = scan_for_secrets(filepath)
                all_violations.extend(file_violations)
                
    # 3. Output the report
    report = {
        "status": "FAILED" if all_violations else "PASSED",
        "total_errors": len(all_violations),
        "errors": all_violations
    }
    
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    run_engine()
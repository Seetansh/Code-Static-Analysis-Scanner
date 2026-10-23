import os
import json
from core.parser import check_project_structure, get_python_files
from core.rules import scan_for_secrets, check_function_length

def run_engine(target_dir):
    if not os.path.exists(target_dir):
        print(f"Error: Directory '{target_dir}' does not exist.")
        return
    
    all_violations = []

    # running structural check on root
    all_violations.extend(check_project_structure(target_dir))
    
    # 1.directory scanning - file level scanning
    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                
                # 2. Running the security scan on each file
                all_violations.extend(scan_for_secrets(filepath))
                all_violations.extend(check_function_length(filepath))
                
    # 3. Output the report
    report = {
        "status": "FAILED" if all_violations else "PASSED",
        "total_errors": len(all_violations),
        "errors": all_violations
    }

    return report

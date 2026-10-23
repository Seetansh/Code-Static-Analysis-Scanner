import os
import re
import json
import ast
import argparse

def scan_for_secrets(filepath):
    violations = []
    # Regex patterns for common secrets
    secret_patterns = [r"sk_live_[a-zA-Z0-9]{24}", r"(password|secret)\s*=\s*['\"].+['\"]"]
    
    with open(filepath, 'r', encoding='utf-8', errors="ignore") as file:
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

def check_function_length(filepath):
    violations = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    try:
        # Parse the code into a syntax tree
        tree = ast.parse(content)
        
        # Walk through every node in the code
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef): # If it's a function
                length = node.end_lineno - node.lineno
                if length > 10: # Fails if longer than 10 lines
                    violations.append({
                        "rule": "QUAL-01",
                        "file": filepath,
                        "line": node.lineno,
                        "message": f"Code Quality: Function '{node.name}' is {length} lines long. Max allowed is 10."
                    })
    except SyntaxError:
        pass # Ignore files with broken Python syntax for now
        
    return violations

def check_project_structure(target_dir):
    violations = []
    required_dirs = {'routes', 'models'}
    
    existing_dirs = set()
    for root, dirs, _ in os.walk(target_dir):
        for d in dirs:
            existing_dirs.add(d)
            
    missing = required_dirs - existing_dirs
    print(missing)
    if missing:
        violations.append({
            "rule": "ARCH-01",
            "file": "Project Root",
            "line": 0,
            "message": f"Architecture: Missing mandatory directories: {list(missing)}. Projects must follow standard layout."
        })
    return violations

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
    
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lightweight Python Static Analysis Scanner")
    parser.add_argument("--path", required=True, help="Path to the target repository directory to scan")
    args = parser.parse_args()
    run_engine(args.path)
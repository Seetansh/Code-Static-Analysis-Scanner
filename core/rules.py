# 3 rules are going to be checked:
"""
1. Hardcoded secrets (like API keys, passwords, etc.) in the codebase.
2. Project must contain specific core folders (like models/, routes/, config.py)
3. No route handler or function should exceed 50 lines of code (to prevent monolithic, unmaintainable mess.)

"""
import re
import ast

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



import os


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

def get_python_files(target_dir):
    py_files = []
    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith('.py'):
                py_files.append(os.path.join(root, file))
    return py_files
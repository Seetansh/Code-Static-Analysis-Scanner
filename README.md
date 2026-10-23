# Lightweight Python Static Analysis Scanner

A modular, lightweight static code analysis and architectural compliance engine built in Python. Designed to inspect student and backend project repositories for security vulnerabilities, code smells, and structural anti-patterns without heavy enterprise overhead.

## Features
- **Security Check (Regex):** Scans source code for hardcoded secrets, API keys, and plaintext credentials (`SEC-01`).
- **AST Code Quality Inspection:** Uses Python's built-in `ast` module to traverse Abstract Syntax Trees and flag bloated, unmaintainable functions (`QUAL-01`).
- **Architectural Layout Verification:** Enforces proper project directory structures (e.g., mandatory `models/` and `routes/` directories).
- **CLI Interface:** Easily run scans on any target repository path directly from the terminal.

## Project Structure
```text
static_code_analysis_scanner/
│
├── core/
│   ├── __init__.py     # Package initializer
│   ├── parser.py       # File system traversal & directory checks
│   ├── rules.py        # Deterministic regex & AST rule implementations
│   └── engine.py       # Orchestration and report generation
│
├── target_repo/        # Test repository sandbox
└── main.py          # CLI entry point
```

## Installation & Usage
1. Clone or download the repository.

2. Run a scan on any target Python repository using the CLI by specifying the path:
```bash
python main.py --path path/to/target_repo
```
## Example JSON Output
The engine outputs a structured JSON report detailing the scan status, total error count, and specific rule violations:

```JSON
{
  "status": "FAILED",
  "total_errors": 2,
  "errors": [
    {
      "rule": "ARCH-01",
      "file": "Project Root",
      "line": 0,
      "message": "Architecture: Missing mandatory directories: ['routes', 'models']."
    },
    {
      "rule": "SEC-01",
      "file": "target_repo/bad_student_code.py",
      "line": 6,
      "message": "CRITICAL: Hardcoded secret detected."
    }
  ]
}
```
## Author

Built as a lightweight open-source utility to bridge the gap between academic projects and real-world software production standards.

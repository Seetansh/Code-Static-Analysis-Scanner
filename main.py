import argparse
import json
from core.engine import run_engine



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lightweight Python Static Analysis Scanner")
    parser.add_argument("--path", required=True, help="Path to the target repository directory to scan")
    args = parser.parse_args()
    report = run_engine(args.path)
    print(json.dumps(report, indent=2))
#!/usr/bin/env python3
"""
CLI entry point for Autonomous Code Reviewer Agent.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.orchestrator import AuditOrchestrator

def main():
    parser = argparse.ArgumentParser(description="Autonomous Code Reviewer Agent CLI")
    parser.add_argument("--file", type=str, default="samples/vulnerable_code.py", help="Python source file to audit")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: File not found at {args.file}")
        sys.exit(1)

    with open(args.file, "r", encoding="utf-8") as f:
        code_content = f.read()

    orchestrator = AuditOrchestrator()
    result = orchestrator.review_code(code_content, filename=args.file)

    print("\n" + "=" * 60)
    print(f"Audit Summary for: {result['filename']}")
    print("=" * 60)
    print(f"Score: {result['health_score']}/100 (Grade: {result['grade']})")
    print(f"Security Findings: {len(result['security_issues'])}")
    print(f"Performance Warnings: {len(result['performance_issues'])}")
    print(f"Quality Warnings: {len(result['quality_issues'])}")
    print(f"Patches Generated: {len(result['patches'])}\n")

if __name__ == "__main__":
    main()

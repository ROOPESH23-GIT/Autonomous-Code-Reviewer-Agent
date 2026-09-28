#!/usr/bin/env python3
"""
🛡️ Autonomous Code Reviewer Agent - Interactive Demo
Demonstrates collaborative multi-agent static code audit and patch synthesis.
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.orchestrator import AuditOrchestrator

def print_banner():
    print("=" * 68)
    print(" 🛡️ AUTONOMOUS CODE REVIEWER AGENT - MULTI-AGENT STATIC AUDIT")
    print("=" * 68)
    print(" Agents: Security Scanner + Performance Optimizer + Quality Enforcer")
    print("-" * 68)

def main():
    print_banner()

    sample_path = os.path.join(os.path.dirname(__file__), "samples", "vulnerable_code.py")
    with open(sample_path, "r", encoding="utf-8") as f:
        code_content = f.read()

    print(f"\n[Audit Target]: {sample_path}")
    print("Initializing Multi-Agent Review Pipeline...\n")
    time.sleep(0.5)

    orchestrator = AuditOrchestrator()
    results = orchestrator.review_code(code_content, filename="samples/vulnerable_code.py")

    print("[Phase 1] 🔒 SecurityScannerAgent Findings:")
    if results["security_issues"]:
        for issue in results["security_issues"]:
            print(f"  🚨 [{issue['severity']}] Line {issue['line']}: {issue['message']}")
            print(f"     Snippet: `{issue['code']}`")
            print(f"     Category: {issue.get('cwe', 'N/A')}\n")
    else:
        print("  ✓ No security vulnerabilities detected.")

    time.sleep(0.5)
    print("[Phase 2] ⚡ PerformanceOptimizerAgent Findings:")
    if results["performance_issues"]:
        for issue in results["performance_issues"]:
            print(f"  ⚠️ [{issue['severity']}] Line {issue['line']}: {issue['message']}")
            print(f"     Snippet: `{issue['code']}`\n")
    else:
        print("  ✓ No algorithmic bottlenecks detected.")

    time.sleep(0.5)
    print("[Phase 3] 📐 QualityEnforcerAgent Findings:")
    if results["quality_issues"]:
        for issue in results["quality_issues"]:
            print(f"  ℹ️ [{issue['severity']}] Line {issue['line']}: {issue['message']}")
    else:
        print("  ✓ Code adheres to quality and documentation standards.")

    time.sleep(0.5)
    print("\n[Phase 4] 🛠️ PatchGeneratorAgent Proposed Remediations:")
    for patch in results["patches"]:
        print(f"  • For Line {patch['target_line']} ({patch['description']}):")
        for line in patch["diff"].split("\n"):
            print(f"      {line}")
        print()

    print("=" * 68)
    print(f" 📊 AUDIT SCORE: {results['health_score']}/100 | CODE GRADE: {results['grade']}")
    print("=" * 68)
    print("✨ Demo completed successfully!\n")

if __name__ == "__main__":
    main()

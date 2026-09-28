import ast
import re

class SecurityScannerAgent:
    """
    Agent responsible for static security inspection using AST analysis and regex pattern matching.
    Detects SQL injection, hardcoded secrets, dangerous builtins (eval/exec).
    """
    def __init__(self):
        self.name = "SecurityScanner"

    def scan(self, code: str) -> list:
        issues = []
        lines = code.split("\n")

        # 1. Regex checks for secrets
        secret_patterns = [
            (r'(?i)(secret|token|password|api[_-]?key)\s*=\s*["\'][a-zA-Z0-9_\-]{8,}["\']', "Exposed hardcoded secret or token credential."),
            (r'AKIA[0-9A-Z]{16}', "Exposed AWS Access Key pattern.")
        ]

        for i, line in enumerate(lines, 1):
            for pattern, desc in secret_patterns:
                if re.search(pattern, line):
                    issues.append({
                        "agent": self.name,
                        "severity": "CRITICAL",
                        "line": i,
                        "code": line.strip(),
                        "message": desc,
                        "cwe": "CWE-798: Use of Hard-coded Credentials"
                    })

        # 2. AST parsing for dangerous patterns
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                # Check for eval() or exec()
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id in ("eval", "exec"):
                        issues.append({
                            "agent": self.name,
                            "severity": "HIGH",
                            "line": getattr(node, "lineno", 0),
                            "code": lines[node.lineno - 1].strip() if hasattr(node, "lineno") else "",
                            "message": f"Dangerous dynamic execution via '{node.func.id}()'. Vulnerable to Arbitrary Code Execution.",
                            "cwe": "CWE-95: Improper Neutralization of Directives in Dynamically Evaluated Code"
                        })

                # Check for SQL concatenation in execute() calls
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Attribute) and node.func.attr == "execute":
                        if node.args and isinstance(node.args[0], (ast.BinOp, ast.JoinedStr)):
                            issues.append({
                                "agent": self.name,
                                "severity": "CRITICAL",
                                "line": getattr(node, "lineno", 0),
                                "code": lines[node.lineno - 1].strip() if hasattr(node, "lineno") else "",
                                "message": "Possible SQL Injection: SQL statement constructed using string concatenation/formatting.",
                                "cwe": "CWE-89: SQL Injection"
                            })
        except SyntaxError as e:
            issues.append({
                "agent": self.name,
                "severity": "ERROR",
                "line": e.lineno,
                "code": "",
                "message": f"Syntax Error: {e.msg}",
                "cwe": "SyntaxError"
            })

        return issues

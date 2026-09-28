import ast

class QualityEnforcerAgent:
    """
    Agent responsible for measuring code maintainability, Cyclomatic Complexity,
    and missing docstrings across functions and classes.
    """
    def __init__(self):
        self.name = "QualityEnforcer"

    def scan(self, code: str) -> list:
        issues = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # 1. Missing docstring check
                    docstring = ast.get_docstring(node)
                    if not docstring:
                        issues.append({
                            "agent": self.name,
                            "severity": "INFO",
                            "line": node.lineno,
                            "function": node.name,
                            "message": f"Function '{node.name}' lacks a descriptive docstring.",
                            "type": "Documentation"
                        })

                    # 2. Cyclomatic Complexity estimation
                    complexity = 1
                    for child in ast.walk(node):
                        if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler, ast.With)):
                            complexity += 1
                        elif isinstance(child, ast.BoolOp):
                            complexity += len(child.values) - 1

                    if complexity > 4:
                        issues.append({
                            "agent": self.name,
                            "severity": "MEDIUM",
                            "line": node.lineno,
                            "function": node.name,
                            "message": f"High Cyclomatic Complexity ({complexity} > threshold 4) in function '{node.name}'. Refactor recommended.",
                            "type": "Maintainability"
                        })
        except Exception:
            pass

        return issues

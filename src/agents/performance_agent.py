import ast

class PerformanceOptimizerAgent:
    """
    Agent responsible for detecting algorithmic bottlenecks, unclosed resources,
    and suboptimal data structure lookups using AST structural walks.
    """
    def __init__(self):
        self.name = "PerformanceOptimizer"

    def scan(self, code: str) -> list:
        issues = []
        lines = code.split("\n")

        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                # Detect Nested Loops -> Potential O(N^2)
                if isinstance(node, (ast.For, ast.While)):
                    for inner in node.body:
                        if isinstance(inner, (ast.For, ast.While)):
                            issues.append({
                                "agent": self.name,
                                "severity": "MEDIUM",
                                "line": getattr(inner, "lineno", node.lineno),
                                "code": lines[inner.lineno - 1].strip() if hasattr(inner, "lineno") else "",
                                "message": "Nested loop detected causing quadratic O(N^2) time complexity. Consider hash set/dict lookups.",
                                "type": "TimeComplexityBottleneck"
                            })

                # Detect open() calls without 'with' context manager
                if isinstance(node, ast.Assign):
                    if isinstance(node.value, ast.Call):
                        if isinstance(node.value.func, ast.Name) and node.value.func.id == "open":
                            issues.append({
                                "agent": self.name,
                                "severity": "LOW",
                                "line": getattr(node, "lineno", 0),
                                "code": lines[node.lineno - 1].strip() if hasattr(node, "lineno") else "",
                                "message": "File descriptor opened without 'with' statement. May cause resource leak.",
                                "type": "UnclosedResource"
                            })
        except Exception:
            pass

        return issues

class PatchGeneratorAgent:
    """
    Agent responsible for synthesizing recommended remediation diffs for identified issues.
    """
    def __init__(self):
        self.name = "PatchGenerator"

    def generate_patches(self, issues: list) -> list:
        patches = []
        for issue in issues:
            if "SQL Injection" in issue.get("message", ""):
                patches.append({
                    "target_line": issue["line"],
                    "description": "Replace string concatenation with parameterized SQL placeholder",
                    "diff": (
                        f"--- Line {issue['line']}\n"
                        f"- cursor.execute(\"SELECT ... WHERE username = '\" + username + \"'\")\n"
                        f"+ cursor.execute(\"SELECT ... WHERE username = ?\", (username,))"
                    )
                })
            elif "Exposed hardcoded secret" in issue.get("message", ""):
                patches.append({
                    "target_line": issue["line"],
                    "description": "Load sensitive credentials securely from environment variables",
                    "diff": (
                        f"--- Line {issue['line']}\n"
                        f"- SECRET = \"...raw_key...\"\n"
                        f"+ import os\n"
                        f"+ SECRET = os.getenv(\"APP_SECRET\", \"\")"
                    )
                })
            elif "Nested loop" in issue.get("message", ""):
                patches.append({
                    "target_line": issue["line"],
                    "description": "Optimize O(N^2) loop to O(N + M) using set intersection",
                    "diff": (
                        f"--- Line {issue['line']}\n"
                        f"- for i in list1:\n"
                        f"-     for j in list2: ...\n"
                        f"+ return list(set(list1).intersection(set(list2)))"
                    )
                })
            elif "File descriptor opened" in issue.get("message", ""):
                patches.append({
                    "target_line": issue["line"],
                    "description": "Use Python context manager to guarantee file closure",
                    "diff": (
                        f"--- Line {issue['line']}\n"
                        f"- f = open('activity.log', 'a')\n"
                        f"+ with open('activity.log', 'a', encoding='utf-8') as f:"
                    )
                })
        return patches

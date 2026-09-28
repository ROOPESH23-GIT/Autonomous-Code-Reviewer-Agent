from .agents.security_agent import SecurityScannerAgent
from .agents.performance_agent import PerformanceOptimizerAgent
from .agents.quality_agent import QualityEnforcerAgent
from .agents.patch_generator_agent import PatchGeneratorAgent

class AuditOrchestrator:
    """
    Coordinates multi-agent code analysis pipeline, aggregates findings,
    calculates code health score, and formats an audit dossier.
    """
    def __init__(self):
        self.security_agent = SecurityScannerAgent()
        self.perf_agent = PerformanceOptimizerAgent()
        self.quality_agent = QualityEnforcerAgent()
        self.patch_agent = PatchGeneratorAgent()

    def review_code(self, source_code: str, filename: str = "target_code.py") -> dict:
        # Run agents in parallel conceptual phases
        sec_issues = self.security_agent.scan(source_code)
        perf_issues = self.perf_agent.scan(source_code)
        quality_issues = self.quality_agent.scan(source_code)

        all_issues = sec_issues + perf_issues + quality_issues

        # Calculate penalty score
        penalty = 0
        for item in all_issues:
            sev = item.get("severity", "LOW")
            if sev == "CRITICAL":
                penalty += 30
            elif sev == "HIGH":
                penalty += 15
            elif sev == "MEDIUM":
                penalty += 8
            elif sev == "LOW":
                penalty += 4
            else:
                penalty += 1

        health_score = max(0, 100 - penalty)

        if health_score >= 90:
            grade = "A"
        elif health_score >= 80:
            grade = "B"
        elif health_score >= 70:
            grade = "C"
        elif health_score >= 60:
            grade = "D"
        else:
            grade = "F"

        patches = self.patch_agent.generate_patches(all_issues)

        return {
            "filename": filename,
            "health_score": health_score,
            "grade": grade,
            "security_issues": sec_issues,
            "performance_issues": perf_issues,
            "quality_issues": quality_issues,
            "total_issues_count": len(all_issues),
            "patches": patches
        }

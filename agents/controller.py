import re
from datetime import datetime


class ControllerAgent:
    """Parses user task, identifies sub-tasks, and creates an execution plan."""

    KEYWORDS = {
        "run_web": ["website", "web", "html", "landing page", "webpage", "site"],
        "run_content": ["ppt", "presentation", "notes", "document", "slides", "write notes", "report"],
        "run_communication": ["reply", "message", "email", "respond", "send", "communicate"],
        "run_chat": ["explain", "help", "what", "how", "who", "suggest", "guide", "talk", "chat", "question"]
    }

    def parse_task(self, task: str) -> dict:
        task_lower = task.lower()
        detected = {}
        log_entries = []
        log_entries.append(f"[{self._ts()}] 🤖 Controller Agent started")
        log_entries.append(f"[{self._ts()}] 📥 Received task: \"{task[:80]}...\"" if len(task) > 80 else f"[{self._ts()}] 📥 Received task: \"{task}\"")

        for flag, kws in self.KEYWORDS.items():
            matched = [kw for kw in kws if kw in task_lower]
            # If the user specifically asks a question and doesn't explicitly want web/ppt, we turn off the others
            detected[flag] = bool(matched)
            if matched:
                log_entries.append(f"[{self._ts()}] ✅ Detected '{flag.replace('run_', '')}' task — keywords: {matched}")

        # If absolutely nothing matched, default to general conversational chat
        if not any(detected.values()):
            detected["run_chat"] = True
            log_entries.append(f"[{self._ts()}] ℹ️ No specific task formats detected, routing to AI Assistant (Chat).")

        # Explicit heuristic: if it's deeply conversational (run_chat match) and NO other flags matched, only run chat
        if detected.get("run_chat") and not (detected.get("run_web") or detected.get("run_content") or detected.get("run_communication")):
             # All clean
             pass
        else:
             # If no chat keywords but other keywords found, we disable chat to avoid noise
             if not any(kw in task_lower for kw in self.KEYWORDS["run_chat"]):
                detected["run_chat"] = False

        log_entries.append(f"[{self._ts()}] 🚀 Dispatching required agents in parallel...")

        return {**detected, "log": log_entries}

    def _ts(self):
        return datetime.utcnow().strftime("%H:%M:%S.%f")[:-3]

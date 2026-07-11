# core/memory.py
import json
from pathlib import Path

class ArceusMemory:
    def __init__(self):
        # Ensure config directory exists
        self.config_dir = Path("D:/Projects/ARCEUS/config")
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.memory_file = self.config_dir / "memory.json"
        self.memory = self._load_memory()

    def _load_memory(self):
        if not self.memory_file.exists():
            # Initialize with your core research parameters
            default_mem = {
                "user_facts": [], 
                "active_research_domain": "modern military IoT and drone network vulnerabilities"
            }
            with open(self.memory_file, "w") as f:
                json.dump(default_mem, f, indent=4)
            return default_mem
        
        with open(self.memory_file, "r") as f:
            return json.load(f)

    def add_fact(self, fact):
        if fact not in self.memory["user_facts"]:
            self.memory["user_facts"].append(fact)
            self._save_memory()

    def _save_memory(self):
        with open(self.memory_file, "w") as f:
            json.dump(self.memory, f, indent=4)
            
    def get_context(self):
        facts = ". ".join(self.memory["user_facts"])
        research = self.memory.get("active_research_domain", "")
        return f"Current Research Focus: {research}. Known Facts: {facts}"
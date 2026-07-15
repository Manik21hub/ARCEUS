# core/plugin_manager.py
import os
import importlib.util
from pathlib import Path

class PluginManager:
    def __init__(self):
        self.plugins = {}
        # Resolves to D:\Projects\ARCEUS\plugins
        self.plugin_dir = Path(__file__).resolve().parent.parent / "plugins"
        self.plugin_dir.mkdir(exist_ok=True)
        self.load_plugins()

    def load_plugins(self):
        """Scans the plugins directory and loads valid modules dynamically."""
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                name = filename[:-3]
                filepath = self.plugin_dir / filename
                
                spec = importlib.util.spec_from_file_location(name, filepath)
                module = importlib.util.module_from_spec(spec)
                try:
                    spec.loader.exec_module(module)
                    # A valid plugin MUST have PLUGIN_META and an execute() function
                    if hasattr(module, 'PLUGIN_META') and hasattr(module, 'execute'):
                        cmd = module.PLUGIN_META['command'].upper()
                        self.plugins[cmd] = {
                            'meta': module.PLUGIN_META,
                            'execute': module.execute
                        }
                        print(f"[System] Plugin Initialized: {module.PLUGIN_META['name']} ({cmd})")
                except Exception as e:
                    print(f"[System Warning] Failed to load plugin {filename}: {e}")

    def get_prompt_injections(self):
        """Generates dynamic instructions for the LLM based on loaded plugins."""
        if not self.plugins:
            return "   - (No dynamic plugins currently loaded)"
        
        lines = []
        for cmd, data in self.plugins.items():
            desc = data['meta'].get('description', 'No description provided.')
            lines.append(f"   - {cmd} (e.g., [CMD:{cmd}|Target]): {desc}")
        return "\n".join(lines)

    def execute_plugin(self, command, target):
        """Routes a command to the appropriate plugin's execute function."""
        cmd = command.upper()
        if cmd in self.plugins:
            try:
                return self.plugins[cmd]['execute'](target)
            except Exception as e:
                print(f"[Plugin Error] {cmd} failed: {e}")
                return False
        return False

# Create a global instance so the Brain and Features share the same memory
plugin_system = PluginManager()
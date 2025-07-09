import os
import importlib.util
from plugins.plugin_base import Plugin

class pluginManager:
    def __init__(self, plugin_dir="plugins"):
        self.plugin_dir = plugin_dir
        self.plugins = []
        
    def load_plugins(self):
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py") and not filename.startswith("__") and filename != "plugin_base.py":
                path = os.path.join(self.plugin_dir, filename)
                name = filename[:-3]
                
                try:
                    spec = importlib.util.spec_from_file_location(name, path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                except Exception as e:
                    print(f"\033[38;2;255;60;60m\nerror loading {name}: {e}\033[0m")
                    continue
                    
                for obj in module.__dict__.values():
                    if isinstance(obj, type) and issubclass(obj, Plugin) and obj is not Plugin:
                        self.plugins.append(obj())
    
    def run_plugins(self, message: str) -> list[str]:
        responses = []
        for plugin in self.plugins:
            if plugin.can_handle(message):
                responses.extend(plugin.handle(message))
                
        return responses
                

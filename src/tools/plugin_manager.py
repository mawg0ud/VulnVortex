import os
import importlib

class PluginManager:
    def __init__(self, plugin_dir="plugins/"):
        self.plugin_dir = plugin_dir

    def list_plugins(self):
        """Lists all available plugins."""
        plugins = [f.split(".")[0] for f in os.listdir(self.plugin_dir) if f.endswith(".py")]
        return plugins

    def load_plugin(self, plugin_name):
        """Dynamically loads a plugin by name."""
        try:
            plugin = importlib.import_module(f"{self.plugin_dir.replace('/', '.')}.{plugin_name}")
            return plugin
        except ImportError as e:
            print(f"Failed to load plugin {plugin_name}: {str(e)}")
            return None

    def activate_plugin(self, plugin_name):
        """Activates and runs a plugin."""
        plugin = self.load_plugin(plugin_name)
        if plugin:
            print(f"Activating plugin: {plugin_name}")
            plugin.run()

if __name__ == "__main__":
    manager = PluginManager()
    available_plugins = manager.list_plugins()
    print(f"Available plugins: {available_plugins}")
    
    plugin_to_activate = input("Enter the plugin to activate: ")
    manager.activate_plugin(plugin_to_activate)

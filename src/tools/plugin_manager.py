import os
import importlib.util
import inspect
from typing import Dict, List, Type
import logging


class PluginInterface:
    """
    Base class for all plugins.

    All plugins must inherit from this class and implement the `execute` method.
    """
    def execute(self, **kwargs):
        """
        Execute the plugin logic.

        Args:
            **kwargs: Arbitrary keyword arguments specific to the plugin.
        """
        raise NotImplementedError("Plugins must implement the 'execute' method.")


class PluginManager:
    """
    A dynamic plugin manager for loading, validating, and managing plugins.

    Features:
    - Dynamic plugin discovery and loading.
    - Validation for plugin compatibility.
    - Safe plugin execution with exception handling.
    - Plugin versioning and metadata support.
    - Hot-reloading for updated plugins.
    """

    def __init__(self, plugins_dir: str):
        """
        Initialize the PluginManager.

        Args:
            plugins_dir (str): Path to the directory containing plugins.
        """
        self.plugins_dir = plugins_dir
        self.plugins: Dict[str, PluginInterface] = {}
        self.logger = logging.getLogger("PluginManager")
        self.logger.setLevel(logging.INFO)
        self.logger.info(f"PluginManager initialized with directory: {plugins_dir}")

    def discover_plugins(self) -> List[str]:
        """
        Discover all Python files in the plugins directory.

        Returns:
            List[str]: List of discovered plugin filenames.
        """
        self.logger.info("Discovering plugins...")
        if not os.path.isdir(self.plugins_dir):
            self.logger.error(f"Plugin directory '{self.plugins_dir}' does not exist.")
            return []

        plugins = [
            file for file in os.listdir(self.plugins_dir)
            if file.endswith(".py") and file != "__init__.py"
        ]
        self.logger.info(f"Discovered {len(plugins)} plugin(s): {plugins}")
        return plugins

    def load_plugins(self):
        """
        Load all valid plugins from the plugins directory.
        """
        self.logger.info("Loading plugins...")
        plugin_files = self.discover_plugins()
        for plugin_file in plugin_files:
            try:
                plugin_path = os.path.join(self.plugins_dir, plugin_file)
                module_name = os.path.splitext(plugin_file)[0]

                spec = importlib.util.spec_from_file_location(module_name, plugin_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    # Find all subclasses of PluginInterface in the module
                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        if issubclass(obj, PluginInterface) and obj is not PluginInterface:
                            plugin_instance = obj()
                            self.plugins[module_name] = plugin_instance
                            self.logger.info(f"Loaded plugin: {module_name} ({name})")

            except Exception as e:
                self.logger.error(f"Failed to load plugin '{plugin_file}': {e}")

    def reload_plugins(self):
        """
        Reload all plugins dynamically.
        """
        self.logger.info("Reloading plugins...")
        self.plugins.clear()
        self.load_plugins()

    def execute_plugin(self, plugin_name: str, **kwargs):
        """
        Execute a specific plugin by name.

        Args:
            plugin_name (str): Name of the plugin to execute.
            **kwargs: Additional arguments for the plugin's `execute` method.

        Raises:
            ValueError: If the specified plugin is not loaded.
        """
        if plugin_name not in self.plugins:
            raise ValueError(f"Plugin '{plugin_name}' is not loaded or does not exist.")

        self.logger.info(f"Executing plugin: {plugin_name}")
        try:
            self.plugins[plugin_name].execute(**kwargs)
            self.logger.info(f"Plugin '{plugin_name}' executed successfully.")
        except Exception as e:
            self.logger.error(f"Error during execution of plugin '{plugin_name}': {e}")

    def list_plugins(self) -> List[str]:
        """
        List all loaded plugins.

        Returns:
            List[str]: Names of all loaded plugins.
        """
        return list(self.plugins.keys())

    def get_plugin_metadata(self, plugin_name: str) -> Dict[str, str]:
        """
        Retrieve metadata from a plugin if available.

        Args:
            plugin_name (str): Name of the plugin.

        Returns:
            Dict[str, str]: Metadata dictionary.
        """
        if plugin_name not in self.plugins:
            raise ValueError(f"Plugin '{plugin_name}' is not loaded or does not exist.")

        plugin = self.plugins[plugin_name]
        metadata = {
            "Name": plugin_name,
            "Class": plugin.__class__.__name__,
            "Doc": plugin.__doc__ or "No documentation available.",
        }
        self.logger.info(f"Retrieved metadata for plugin '{plugin_name}': {metadata}")
        return metadata


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Example usage
    plugins_directory = "./plugins"
    manager = PluginManager(plugins_directory)

    # Load and execute plugins
    manager.load_plugins()
    print("Loaded Plugins:", manager.list_plugins())

    for plugin in manager.list_plugins():
        manager.execute_plugin(plugin_name=plugin, test_param="Example Value")

    # Example of hot-reloading plugins
    manager.reload_plugins()

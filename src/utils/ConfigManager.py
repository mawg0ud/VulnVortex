import yaml
import os

class ConfigManager:
    def __init__(self, config_file="config/config.yaml"):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        """Loads and returns the configuration from the YAML file."""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return yaml.safe_load(f)
        else:
            raise FileNotFoundError(f"{self.config_file} does not exist.")

    def validate_config(self):
        """Validates mandatory fields in the config."""
        required_keys = ['network', 'vulnerability_database', 'scheduler']
        for key in required_keys:
            if key not in self.config:
                raise KeyError(f"Mandatory config section {key} missing")

    def update_config(self, key, value):
        """Dynamically updates a config value."""
        keys = key.split('.')
        conf = self.config
        for k in keys[:-1]:
            conf = conf[k]
        conf[keys[-1]] = value
        self.save_config()

    def save_config(self):
        """Saves the updated configuration back to the YAML file."""
        with open(self.config_file, 'w') as f:
            yaml.dump(self.config, f)

if __name__ == "__main__":
    config_manager = ConfigManager()
    config_manager.validate_config()
    config_manager.update_config("network.scan_ports", "80,443")

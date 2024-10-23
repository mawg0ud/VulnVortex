import requests
import os
import yaml

class VulnDBUpdater:
    def __init__(self, config_file="config/config.yaml"):
        self.config = self.load_config(config_file)
        self.vuln_sources = self.config['vulnerability_database']['sources']
        self.update_frequency = self.config['vulnerability_database']['update_frequency']
        self.save_path = os.path.join("data", "vuln_db")

    def load_config(self, config_file):
        """Loads configuration file (YAML)"""
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)

    def fetch_updates(self):
        """Fetches updates from all configured sources."""
        for source in self.vuln_sources:
            if source['enabled']:
                print(f"Fetching updates from {source['name']}...")
                self.fetch_from_source(source)

    def fetch_from_source(self, source):
        """Fetches vulnerability data from a specific source."""
        headers = {"Authorization": f"Bearer {source['api_key']}"}
        response = requests.get(source['url'], headers=headers)
        
        if response.status_code == 200:
            self.save_data(source['name'], response.json())
        else:
            print(f"Failed to fetch data from {source['name']}: {response.status_code}")

    def save_data(self, source_name, data):
        """Saves the fetched vulnerability data to a file."""
        os.makedirs(self.save_path, exist_ok=True)
        file_path = os.path.join(self.save_path, f"{source_name}.json")
        with open(file_path, 'w') as f:
            f.write(data)
        print(f"Data saved for {source_name}")

if __name__ == "__main__":
    updater = VulnDBUpdater()
    updater.fetch_updates()

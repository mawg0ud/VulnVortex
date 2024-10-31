import requests
import yaml

class APIIntegration:
    def __init__(self, config_file="config/config.yaml"):
        self.config = self.load_config(config_file)
        self.shodan_api_key = self.config['third_party_services']['shodan']['api_key']
        self.censys_api_key = self.config['third_party_services']['censys']['api_key']

    def load_config(self, config_file):
        """Loads configuration from a YAML file."""
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)

    def query_shodan(self, target_ip):
        """Queries Shodan for detailed information about a target IP."""
        url = f"https://api.shodan.io/shodan/host/{target_ip}?key={self.shodan_api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Shodan data for {target_ip}: {response.json()}")
        else:
            print(f"Failed to fetch data from Shodan: {response.status_code}")

    def query_censys(self, target_ip):
        """Queries Censys for detailed information about a target IP."""
        url = f"https://censys.io/api/v1/view/ipv4/{target_ip}"
        headers = {"Authorization": f"Bearer {self.censys_api_key}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(f"Censys data for {target_ip}: {response.json()}")
        else:
            print(f"Failed to fetch data from Censys: {response.status_code}")

if __name__ == "__main__":
    api = APIIntegration()
    api.query_shodan("192.168.1.1")
    api.query_censys("192.168.1.1")
api_integration.py

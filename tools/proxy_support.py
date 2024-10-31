import requests
import yaml

class ProxyManager:
    def __init__(self, config_file="config/config.yaml"):
        self.config = self.load_config(config_file)
        self.proxies = self.config.get("network", {}).get("proxy", {})

    def load_config(self, config_file):
        """Load proxy configurations from YAML file."""
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)

    def make_request(self, url):
        """Make a network request using proxy settings."""
        try:
            response = requests.get(url, proxies=self.proxies)
            if response.status_code == 200:
                return response.content
            else:
                print(f"Request failed: {response.status_code}")
        except requests.exceptions.ProxyError:
            print("Proxy error occurred.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    proxy_manager = ProxyManager()
    data = proxy_manager.make_request("http://example.com")
    if data:
        print("Request successful.")

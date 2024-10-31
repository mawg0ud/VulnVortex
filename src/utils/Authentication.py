import requests
import yaml

class Authentication:
    def __init__(self, config_file="config/config.yaml"):
        self.config = self.load_config(config_file)
        self.api_keys = self.config['api_keys']
        self.oauth_token = None

    def load_config(self, config_file):
        """Loads the configuration."""
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)

    def get_api_key(self, service_name):
        """Returns the API key for a service."""
        return self.api_keys.get(service_name, None)

    def authenticate_oauth(self, client_id, client_secret, token_url):
        """Authenticate using OAuth and get a token."""
        data = {'client_id': client_id, 'client_secret': client_secret, 'grant_type': 'client_credentials'}
        response = requests.post(token_url, data=data)
        if response.status_code == 200:
            self.oauth_token = response.json().get("access_token")
            return self.oauth_token
        else:
            raise Exception("Failed to authenticate with OAuth")

if __name__ == "__main__":
    auth = Authentication()
    token = auth.authenticate_oauth("your_client_id", "your_client_secret", "https://oauth.server/token")
    print(f"OAuth Token: {token}")

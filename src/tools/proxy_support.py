import requests
from typing import Optional, Dict
import logging


class ProxySupport:
    """
    A robust and versatile proxy management system.

    Features:
    - Automatic proxy validation.
    - Fallback to backup proxies on failure.
    - Supports HTTP, HTTPS, and SOCKS proxies.
    - Dynamic proxy rotation.
    - Logging and monitoring of proxy performance.
    """

    def __init__(self, proxies: Optional[Dict[str, str]] = None, validate_on_init: bool = True):
        """
        Initialize ProxySupport with optional proxies and validation.

        Args:
            proxies (Dict[str, str]): A dictionary of proxies with the format:
                {
                    "http": "http://proxy1.example.com:8080",
                    "https": "http://proxy2.example.com:8080"
                }
            validate_on_init (bool): Validate proxies during initialization.
        """
        self.logger = logging.getLogger("ProxySupport")
        self.logger.setLevel(logging.INFO)

        self.proxies = proxies or {}
        self.active_proxy = None

        if validate_on_init:
            self.logger.info("Validating initial proxies.")
            self.validate_proxies()

    def add_proxy(self, proxy_type: str, proxy_url: str):
        """
        Add a new proxy to the pool.

        Args:
            proxy_type (str): The type of proxy (e.g., 'http', 'https', 'socks5').
            proxy_url (str): The proxy URL (e.g., 'http://proxy.example.com:8080').
        """
        self.logger.info(f"Adding proxy: {proxy_type} -> {proxy_url}")
        self.proxies[proxy_type] = proxy_url

    def validate_proxies(self) -> None:
        """
        Validate all configured proxies and log their status.
        """
        self.logger.info("Validating proxies...")
        for proxy_type, proxy_url in list(self.proxies.items()):
            if not self._is_proxy_valid(proxy_type, proxy_url):
                self.logger.warning(f"Invalid proxy removed: {proxy_type} -> {proxy_url}")
                del self.proxies[proxy_type]

    def _is_proxy_valid(self, proxy_type: str, proxy_url: str) -> bool:
        """
        Check if a proxy is valid by making a test request.

        Args:
            proxy_type (str): The type of proxy (e.g., 'http', 'https', 'socks5').
            proxy_url (str): The proxy URL to validate.

        Returns:
            bool: True if the proxy is valid, False otherwise.
        """
        self.logger.info(f"Testing proxy: {proxy_type} -> {proxy_url}")
        test_url = "https://httpbin.org/ip"
        proxies = {proxy_type: proxy_url}

        try:
            response = requests.get(test_url, proxies=proxies, timeout=5)
            if response.status_code == 200:
                self.logger.info(f"Proxy valid: {proxy_url} -> {response.json()}")
                return True
        except Exception as e:
            self.logger.error(f"Proxy validation failed for {proxy_url}: {e}")
        return False

    def rotate_proxy(self):
        """
        Rotate to the next available proxy.
        """
        if not self.proxies:
            self.logger.error("No proxies available for rotation.")
            return None

        self.logger.info("Rotating proxies...")
        proxy_list = list(self.proxies.values())
        if self.active_proxy:
            current_index = proxy_list.index(self.active_proxy)
            next_index = (current_index + 1) % len(proxy_list)
            self.active_proxy = proxy_list[next_index]
        else:
            self.active_proxy = proxy_list[0]

        self.logger.info(f"Active proxy set to: {self.active_proxy}")
        return self.active_proxy

    def get_active_proxy(self) -> Optional[Dict[str, str]]:
        """
        Retrieve the currently active proxy.

        Returns:
            Dict[str, str]: The active proxy in the format required by `requests`.
        """
        if self.active_proxy:
            for proxy_type, proxy_url in self.proxies.items():
                if proxy_url == self.active_proxy:
                    return {proxy_type: proxy_url}
        self.logger.warning("No active proxy is set.")
        return None

    def fetch_with_proxy(self, url: str, **kwargs) -> Optional[requests.Response]:
        """
        Make an HTTP request using the active proxy.

        Args:
            url (str): The URL to fetch.
            **kwargs: Additional arguments for `requests.get`.

        Returns:
            requests.Response: The HTTP response object, or None if the request fails.
        """
        self.logger.info(f"Fetching URL with proxy: {url}")
        active_proxy = self.get_active_proxy()

        if not active_proxy:
            self.logger.error("No active proxy available. Request aborted.")
            return None

        try:
            response = requests.get(url, proxies=active_proxy, timeout=10, **kwargs)
            self.logger.info(f"Request successful: {response.status_code}")
            return response
        except Exception as e:
            self.logger.error(f"Request failed with active proxy: {e}")
            self.rotate_proxy()
            return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Example usage
    proxies_config = {
        "http": "http://proxy1.example.com:8080",
        "https": "http://proxy2.example.com:8080",
    }
    proxy_manager = ProxySupport(proxies=proxies_config)

    # Validate proxies
    proxy_manager.validate_proxies()

    # Rotate and fetch using proxies
    proxy_manager.rotate_proxy()
    response = proxy_manager.fetch_with_proxy("https://httpbin.org/ip")
    if response:
        print(response.json())

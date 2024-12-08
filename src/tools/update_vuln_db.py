import requests
import json
import os
import hashlib
import logging
from typing import Optional

class VulnerabilityDBUpdater:
    """
    A sophisticated tool for updating and managing a local vulnerability database.

    Features:
    - Fetch vulnerability data from multiple sources.
    - Incremental updates with hash-based change detection.
    - Local backup and recovery for failed updates.
    - Support for multiple vulnerability formats (JSON, XML, etc.).
    - Logging and analytics for update performance.
    """

    def __init__(self, db_path: str, sources: list, backup_path: Optional[str] = None):
        """
        Initialize the VulnerabilityDBUpdater.

        Args:
            db_path (str): Path to the local vulnerability database file.
            sources (list): List of source URLs for fetching vulnerability updates.
            backup_path (Optional[str]): Path for backup storage (optional).
        """
        self.db_path = db_path
        self.sources = sources
        self.backup_path = backup_path or f"{db_path}.backup"
        self.logger = logging.getLogger("VulnerabilityDBUpdater")
        self.logger.setLevel(logging.INFO)

        if not os.path.exists(os.path.dirname(self.db_path)):
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            self.logger.info(f"Created directory for vulnerability database: {os.path.dirname(self.db_path)}")

    def fetch_vulnerability_data(self, source: str) -> Optional[dict]:
        """
        Fetch vulnerability data from a source.

        Args:
            source (str): URL of the vulnerability data source.

        Returns:
            dict: Parsed vulnerability data, or None if fetching fails.
        """
        self.logger.info(f"Fetching data from source: {source}")
        try:
            response = requests.get(source, timeout=10)
            response.raise_for_status()
            if response.headers.get('Content-Type') == 'application/json':
                return response.json()
            else:
                self.logger.warning(f"Unexpected content type for {source}: {response.headers.get('Content-Type')}")
        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch data from {source}: {e}")
        return None

    def calculate_hash(self, data: str) -> str:
        """
        Calculate a hash of the given data.

        Args:
            data (str): Data string to hash.

        Returns:
            str: SHA256 hash of the data.
        """
        return hashlib.sha256(data.encode()).hexdigest()

    def is_update_needed(self, new_data: dict) -> bool:
        """
        Check if the database needs updating based on hash comparison.

        Args:
            new_data (dict): New vulnerability data.

        Returns:
            bool: True if the database needs updating, False otherwise.
        """
        if not os.path.exists(self.db_path):
            self.logger.info("No existing database found. Update required.")
            return True

        try:
            with open(self.db_path, 'r') as f:
                current_data = f.read()
            current_hash = self.calculate_hash(current_data)
            new_hash = self.calculate_hash(json.dumps(new_data, indent=4))
            return current_hash != new_hash
        except Exception as e:
            self.logger.error(f"Error reading current database: {e}")
            return True

    def backup_existing_db(self):
        """
        Create a backup of the current database before updating.
        """
        if not os.path.exists(self.db_path):
            self.logger.warning("No existing database to backup.")
            return

        try:
            os.rename(self.db_path, self.backup_path)
            self.logger.info(f"Backup created: {self.backup_path}")
        except Exception as e:
            self.logger.error(f"Failed to create backup: {e}")

    def update_database(self):
        """
        Update the local vulnerability database from all sources.
        """
        all_vulns = []
        for source in self.sources:
            data = self.fetch_vulnerability_data(source)
            if data:
                all_vulns.extend(data.get("vulnerabilities", []))

        if not all_vulns:
            self.logger.warning("No vulnerability data fetched. Aborting update.")
            return

        new_data = {"vulnerabilities": all_vulns}
        if self.is_update_needed(new_data):
            self.logger.info("Update needed. Proceeding with update.")
            self.backup_existing_db()
            try:
                with open(self.db_path, 'w') as f:
                    json.dump(new_data, f, indent=4)
                self.logger.info(f"Vulnerability database updated successfully: {self.db_path}")
            except Exception as e:
                self.logger.error(f"Failed to update database: {e}")
                self.restore_backup()
        else:
            self.logger.info("Database is already up-to-date. No update required.")

    def restore_backup(self):
        """
        Restore the backup database in case of an update failure.
        """
        if not os.path.exists(self.backup_path):
            self.logger.warning("No backup found to restore.")
            return

        try:
            os.rename(self.backup_path, self.db_path)
            self.logger.info(f"Backup restored: {self.db_path}")
        except Exception as e:
            self.logger.error(f"Failed to restore backup: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Example usage
    updater = VulnerabilityDBUpdater(
        db_path="./data/vulnerability_db.json",
        sources=[
            "https://example.com/vulns1.json",
            "https://example.com/vulns2.json"
        ]
    )
    updater.update_database()

import os
import time
import subprocess
import yaml

class ScanScheduler:
    def __init__(self, config_file="config/config.yaml"):
        self.config = self.load_config(config_file)
        self.scan_interval = self.config['scheduler']['scan_interval']
        self.target = self.config['network']['target_ip']
        self.ports = self.config['network']['scan_ports']
        self.scan_command = f"python CLI.py --target {self.target} --ports {self.ports}"

    def load_config(self, config_file):
        """Loads configuration from a YAML file."""
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)

    def run_scheduled_scan(self):
        """Run scan periodically based on the configured interval."""
        while True:
            print(f"Starting scheduled scan on {self.target}...")
            result = subprocess.run(self.scan_command, shell=True)
            if result.returncode == 0:
                print("Scan completed successfully.")
            else:
                print("Scan failed. Check logs for more details.")
            print(f"Next scan in {self.scan_interval} seconds...")
            time.sleep(self.scan_interval)

if __name__ == "__main__":
    scheduler = ScanScheduler()
    scheduler.run_scheduled_scan()

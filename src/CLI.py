import argparse
from src.core.Scanner import Scanner
from src.utils.ConfigManager import ConfigManager
from src.core.ReportGenerator import ReportGenerator

class CLI:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.scanner = Scanner(self.config_manager.config)

    def run(self):
        parser = argparse.ArgumentParser(description="Vulnerability Scanner CLI")
        parser.add_argument("-s", "--scan", help="IP range to scan (e.g., 192.168.1.0/24)", required=True)
        parser.add_argument("-o", "--output", help="Output report format (e.g., html, txt)", default="html")
        args = parser.parse_args()

        print(f"Starting scan on {args.scan}...")
        vulnerabilities = self.scanner.scan_network(args.scan)
        
        if vulnerabilities:
            print(f"Scan completed. Found {len(vulnerabilities)} vulnerabilities.")
            report_gen = ReportGenerator(output_format=args.output)
            report_gen.generate(vulnerabilities)
            print(f"Report saved in {self.config_manager.config['reporting']['output_directory']}")
        else:
            print("No vulnerabilities found.")

if __name__ == "__main__":
    cli = CLI()
    cli.run()

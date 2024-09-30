# Scanner.py

import subprocess
import json
from abc import ABC, abstractmethod
import logging

# Setup logging for the scanner module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ScanResult:
    """
    Class to encapsulate the results of a scan.
    This will store data such as raw output, parsed vulnerabilities, and any metadata.
    """
    def __init__(self, target, scan_type, raw_output):
        self.target = target
        self.scan_type = scan_type
        self.raw_output = raw_output
        self.parsed_data = None

    def parse(self):
        """
        Method to be implemented in subclasses for parsing raw scan output.
        """
        raise NotImplementedError("Parse method must be implemented by subclasses")

    def to_json(self):
        """
        Converts parsed data to a JSON string for report generation or further processing.
        """
        if self.parsed_data:
            return json.dumps(self.parsed_data, indent=4)
        else:
            logging.warning(f"No parsed data available for target {self.target}")
            return json.dumps({"error": "No parsed data"})

    def __str__(self):
        return f"ScanResult(target={self.target}, scan_type={self.scan_type})"


class Scanner(ABC):
    """
    Abstract Base Scanner class that defines the common interface for all types of scanners.
    Each specific scanner (e.g., Nmap, Web) will extend this class.
    """
    def __init__(self, target):
        self.target = target
        self.result = None

    @abstractmethod
    def scan(self):
        """
        Abstract scan method to be implemented by subclasses.
        It should perform the scan and return an instance of ScanResult.
        """
        pass

    def validate_target(self):
        """
        Validates if the target (e.g., an IP address or domain) is reachable or valid.
        This is a basic check and should be overridden for more specific needs.
        """
        logging.info(f"Validating target: {self.target}")
        if isinstance(self.target, str) and self.target:
            return True
        else:
            logging.error(f"Invalid target: {self.target}")
            raise ValueError("Invalid target. It must be a non-empty string.")


class NmapScanner(Scanner):
    """
    Nmap Scanner class for network scanning. Inherits from the Scanner base class.
    Utilizes Nmap command-line tool to perform the scan.
    """
    def __init__(self, target, options='-sV'):
        super().__init__(target)
        self.options = options  # Allow users to specify Nmap options
        self.validate_target()

    def scan(self):
        """
        Performs an Nmap scan on the given target using the specified options.
        Returns a ScanResult object containing the raw output and parsed data.
        """
        command = f"nmap {self.options} {self.target}"
        logging.info(f"Running Nmap scan with command: {command}")
        
        try:
            # Run the Nmap command
            raw_output = subprocess.check_output(command, shell=True, universal_newlines=True)
            logging.info(f"Nmap scan completed successfully for target: {self.target}")

            # Create a ScanResult instance with the raw Nmap output
            self.result = NmapScanResult(self.target, raw_output)
            self.result.parse()  # Attempt to parse the Nmap output
            return self.result

        except subprocess.CalledProcessError as e:
            logging.error(f"Nmap scan failed for target {self.target}: {e}")
            raise RuntimeError(f"Failed to execute Nmap scan: {e}")


class NmapScanResult(ScanResult):
    """
    Class to handle and parse Nmap scan results.
    Inherits from ScanResult and provides specialized parsing logic for Nmap output.
    """
    def __init__(self, target, raw_output):
        super().__init__(target, "Nmap", raw_output)

    def parse(self):
        """
        Parses raw Nmap output to extract meaningful data like open ports and services.
        For simplicity, we are simulating the parsing.
        """
        logging.info(f"Parsing Nmap scan output for target: {self.target}")
        # Simplified parsing logic (you could expand this to a real parser)
        open_ports = []
        for line in self.raw_output.splitlines():
            if "open" in line:
                open_ports.append(line.strip())
        
        self.parsed_data = {
            "target": self.target,
            "open_ports": open_ports,
            "scan_type": self.scan_type
        }
        logging.info(f"Parsed {len(open_ports)} open ports for target: {self.target}")


class WebScanner(Scanner):
    """
    WebScanner class for web application scanning.
    Inherits from Scanner and can integrate with tools like Nikto, or custom scripts.
    """
    def __init__(self, target):
        super().__init__(target)
        self.validate_target()

    def scan(self):
        """
        Performs a basic web scan (this is a placeholder for a more advanced scanner).
        Could integrate with tools like Nikto or a custom web vulnerability scanning engine.
        """
        logging.info(f"Running Web scan for target: {self.target}")
        # Simulate web scan output
        raw_output = f"Simulated web scan result for {self.target}"
        self.result = WebScanResult(self.target, raw_output)
        self.result.parse()  # Attempt to parse the web scan output
        return self.result


class WebScanResult(ScanResult):
    """
    Class to handle and parse Web scan results.
    Inherits from ScanResult and provides specialized parsing logic for web vulnerability outputs.
    """
    def __init__(self, target, raw_output):
        super().__init__(target, "Web", raw_output)

    def parse(self):
        """
        Simulates parsing of web scan results. In reality, you'd implement parsing based on the tool's output format.
        """
        logging.info(f"Parsing Web scan output for target: {self.target}")
        # Simulated parsing logic
        vulnerabilities = ["XSS", "SQL Injection"]
        self.parsed_data = {
            "target": self.target,
            "vulnerabilities": vulnerabilities,
            "scan_type": self.scan_type
        }
        logging.info(f"Parsed {len(vulnerabilities)} vulnerabilities for target: {self.target}")

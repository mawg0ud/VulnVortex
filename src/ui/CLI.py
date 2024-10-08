import argparse
import logging
import os
from Scanner import Scanner
from VulnerabilityScanner import VulnerabilityScanner
from Exploitation import ExploitManager, CVEExploiter, CustomExploiter
from ReportGenerator import ReportGenerator

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class CommandLineInterface:
    """
    The CommandLineInterface class manages user input through the command-line and orchestrates
    the workflow of scanning, exploitation, and report generation.
    """
    
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='Vulnerability Scanner and Exploitation Tool',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        self.setup_arguments()

    def setup_arguments(self):
        """
        Configures command-line arguments and options for the tool.
        """
        subparsers = self.parser.add_subparsers(dest="command", help="Available commands")

        # Scan command
        scan_parser = subparsers.add_parser("scan", help="Scan the network or target system for open ports and services")
        scan_parser.add_argument("-t", "--target", required=True, help="Target IP or host to scan")
        scan_parser.add_argument("-p", "--ports", default="1-65535", help="Port range to scan (default: 1-65535)")
        scan_parser.add_argument("-o", "--output", default=None, help="Output file to save scan results")

        # Vulnerability Scan command
        vuln_scan_parser = subparsers.add_parser("vuln_scan", help="Scan the target for vulnerabilities")
        vuln_scan_parser.add_argument("-t", "--target", required=True, help="Target IP or host for vulnerability scanning")
        vuln_scan_parser.add_argument("-s", "--scan-result", required=True, help="Input scan result file for vulnerability detection")

        # Exploit command
        exploit_parser = subparsers.add_parser("exploit", help="Exploit known vulnerabilities on the target")
        exploit_parser.add_argument("-t", "--target", required=True, help="Target IP or host for exploitation")
        exploit_parser.add_argument("-v", "--vulns", required=True, help="Vulnerabilities file (JSON format) to exploit")

        # Report command
        report_parser = subparsers.add_parser("report", help="Generate a report of the exploitation results")
        report_parser.add_argument("-t", "--target", required=True, help="Target IP or host for generating the report")
        report_parser.add_argument("-r", "--results", required=True, help="Exploitation results file (JSON format)")
        report_parser.add_argument("-f", "--format", required=True, choices=["json", "html", "pdf", "text"], help="Report format")
        report_parser.add_argument("-o", "--output", default="report", help="Output file name for the generated report")
        report_parser.add_argument("--template", default=None, help="Custom HTML template for the report (if applicable)")

    def run(self):
        """
        Parses command-line arguments and calls the appropriate functionality based on the command.
        """
        args = self.parser.parse_args()
        
        if args.command == "scan":
            self.run_scan(args.target, args.ports, args.output)
        elif args.command == "vuln_scan":
            self.run_vuln_scan(args.target, args.scan_result)
        elif args.command == "exploit":
            self.run_exploit(args.target, args.vulns)
        elif args.command == "report":
            self.run_report(args.target, args.results, args.format, args.output, args.template)
        else:
            self.parser.print_help()

    def run_scan(self, target, ports, output_file):
        """
        Runs a network or system scan for open ports and services.
        """
        logging.info(f"Starting scan on target: {target} for ports: {ports}")
        scanner = Scanner(target, ports)
        scan_results = scanner.perform_scan()
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(scan_results)
            logging.info(f"Scan results saved to {output_file}")
        else:
            print(scan_results)

    def run_vuln_scan(self, target, scan_result_file):
        """
        Runs vulnerability detection on the target based on the scan results.
        """
        logging.info(f"Running vulnerability scan on target: {target} using scan results from {scan_result_file}")
        
        if not os.path.exists(scan_result_file):
            logging.error(f"Scan result file {scan_result_file} does not exist")
            return
        
        # Initialize vulnerability scanner
        vuln_scanner = VulnerabilityScanner(target, scan_result_file)
        vulnerabilities = vuln_scanner.detect_vulnerabilities()
        
        # Print or save the vulnerabilities
        for vuln in vulnerabilities:
            print(f"Vulnerability: {vuln}")

    def run_exploit(self, target, vulns_file):
        """
        Runs exploits on the target based on known vulnerabilities.
        """
        logging.info(f"Running exploitation on target: {target} using vulnerabilities file {vulns_file}")
        
        if not os.path.exists(vulns_file):
            logging.error(f"Vulnerabilities file {vulns_file} does not exist")
            return

        # Load vulnerabilities from the file
        with open(vulns_file, 'r') as file:
            vulnerabilities = json.load(file)

        # Initialize ExploitManager and execute exploits
        exploit_manager = ExploitManager(target, vulnerabilities)
        results = exploit_manager.run_exploits()

        # Save the results in JSON format
        results_file = f"exploit_results_{target}.json"
        with open(results_file, 'w') as file:
            json.dump([result.to_json() for result in results], file, indent=4)
        logging.info(f"Exploitation results saved to {results_file}")

    def run_report(self, target, results_file, format_type, output_file, template_file=None):
        """
        Generates a report based on the exploitation results.
        """
        logging.info(f"Generating {format_type.upper()} report for target {target} using results from {results_file}")
        
        if not os.path.exists(results_file):
            logging.error(f"Results file {results_file} does not exist")
            return

        # Load results from file
        with open(results_file, 'r') as file:
            results_data = json.load(file)

        # Initialize ReportGenerator and generate the report
        report_generator = ReportGenerator(format_type=format_type, template_file=template_file)
        report_content = report_generator.generate_report(results_data)
        
        # Save the report to a file
        output_path = f"{output_file}.{format_type}"
        if format_type == "pdf":
            with open(output_path, 'wb') as file:
                file.write(report_content)
        else:
            with open(output_path, 'w') as file:
                file.write(report_content)
        logging.info(f"Report saved to {output_path}")


# Entry point for the CLI
if __name__ == "__main__":
    cli = CommandLineInterface()
    cli.run()

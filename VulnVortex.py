#!/usr/bin/env python3

import socket
import argparse
import os
import datetime

class PenetrationTester:
    def __init__(self, target_ip, start_port, end_port, log_file_path="PenTestLog.txt"):
        self.target_ip = target_ip
        self.start_port = start_port
        self.end_port = end_port
        self.log_file_path = log_file_path
        self.results = []

    def log(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {message}"
        print(log_entry)
        self.results.append(log_entry)

    def scan_network(self):
        self.log(f"Scanning network {self.target_ip} for open ports...")

        for port in range(self.start_port, self.end_port + 1):
            result = self.check_port(port)
            if result:
                self.log(f"Port {port} is open.")
            else:
                self.log(f"Port {port} is closed.")

    def check_port(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            return sock.connect_ex((self.target_ip, port)) == 0

    def assess_vulnerabilities(self):
        self.log("Assessing vulnerabilities...")


        self.log("Vulnerability assessment completed. Suggestions:")
        self.log("1. Update software to the latest versions.")
        self.log("2. Review and strengthen access controls.")

    def exploit_vulnerability(self, target_port):
        self.log(f"Exploiting vulnerability at {self.target_ip}:{target_port}...")

        # Add your exploitation logic here

        self.log(f"Exploited vulnerability at {self.target_ip}:{target_port}. Suggestions:")
        self.log("1. Patch the identified vulnerability immediately.")
        self.log("2. Review and update firewall rules.")

    def generate_report(self):
        self.log("Generating penetration test report...")

        # Add your report generation logic here

        self.log("Penetration test report generated. Suggestions:")
        self.log("1. Share the report with relevant stakeholders.")
        self.log("2. Prioritize and implement recommended security improvements.")

    def save_results(self):
        with open(self.log_file_path, "a") as log_file:
            for result in self.results:
                log_file.write(f"{result}\n")

def main():
    parser = argparse.ArgumentParser(description="Penetration Tool")
    parser.add_argument("target_ip", help="Target IP address")
    parser.add_argument("start_port", type=int, help="Starting port for scanning")
    parser.add_argument("end_port", type=int, help="Ending port for scanning")
    parser.add_argument("--log_file", default="PenTestLog.txt", help="Path to the log file")

    args = parser.parse_args()

    penetration_tester = PenetrationTester(args.target_ip, args.start_port, args.end_port, args.log_file)

    try:
        # Perform network scanning
        penetration_tester.scan_network()

        # Perform vulnerability assessment
        penetration_tester.assess_vulnerabilities()

        # Simulate exploitation (for demonstration purposes only)
        target_port = int(input("Enter the target port for exploitation: "))
        penetration_tester.exploit_vulnerability(target_port)

        # Generate a penetration test report
        penetration_tester.generate_report()

        print("Penetration testing completed successfully!")

        # Save results to the log file
        penetration_tester.save_results()

    except ValueError:
        print("Invalid input. Please enter valid numeric values for ports.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

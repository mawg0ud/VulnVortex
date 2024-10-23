#### **API Documentation**

**1. Scanner Class:**
   - **Method: `perform_scan(self)`**
     - Description: Scans the target for open ports and services.
     - Parameters:
       - `target` (str): The target IP or hostname.
       - `ports` (str): Ports to scan (e.g., `1-65535`).
     - Returns:
       - A string with scan results.
     - Example:
       ```python
       scanner = Scanner("192.168.1.1", "1-1000")
       results = scanner.perform_scan()
       ```

**2. VulnerabilityScanner Class:**
   - **Method: `detect_vulnerabilities(self)`**
     - Description: Detects vulnerabilities based on the scanned services.
     - Parameters:
       - `target` (str): The target IP or hostname.
       - `scan_file` (str): File containing previous scan results.
     - Returns:
       - A list of detected vulnerabilities.
     - Example:
       ```python
       vuln_scanner = VulnerabilityScanner("192.168.1.1", "scan_results.json")
       vulns = vuln_scanner.detect_vulnerabilities()
       ```

**3. ExploitManager Class:**
   - **Method: `run_exploits(self)`**
     - Description: Executes available exploits against the detected vulnerabilities.
     - Parameters:
       - `target` (str): The target IP or hostname.
       - `vulnerabilities` (list): List of vulnerabilities detected.
     - Returns:
       - A list of exploit results.
     - Example:
       ```python
       exploit_manager = ExploitManager("192.168.1.1", vulnerabilities)
       results = exploit_manager.run_exploits()
       ```

**4. ReportGenerator Class:**
   - **Method: `generate_report(self, results)`**
     - Description: Generates a report in the specified format.
     - Parameters:
       - `results` (dict): Scan and exploit results.
       - `format` (str): Output format (`json`, `html`, `pdf`, `text`).
     - Returns:
       - Report content in the desired format.
     - Example:
       ```python
       report_generator = ReportGenerator("pdf")
       report_content = report_generator.generate_report(results)
       ```

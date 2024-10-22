
#### **Usage Examples and Tutorials**

**1. Basic Scanning Example:**
   ```bash
   python CLI.py --target 192.168.1.1 --ports 80,443
   ```
   - Output will show open ports, services, and basic scan information.

**2. Vulnerability Detection Example:**
   ```bash
   python CLI.py --target 192.168.1.1 --vuln-scan
   ```
   - This runs a vulnerability scan on the target using detected services and ports.

**3. Exploitation Example:**
   ```bash
   python CLI.py --target 192.168.1.1 --exploit
   ```
   - This attempts exploitation based on vulnerabilities found in the previous step.

**4. GUI Usage:**
   - Run the graphical user interface:
     ```bash
     python GUI.py
     ```
   - Use the interface to run scans, detect vulnerabilities, and generate reports.

**5. Report Generation Example:**
   ```bash
   python CLI.py --target 192.168.1.1 --report pdf --output report.pdf
   ```
   - Generates a detailed PDF report of the scan and vulnerability findings.

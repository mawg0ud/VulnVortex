#### **Integration with External Tools**

**1. Nmap Integration:**
   - Nmap is used as the core port scanning engine. Ensure it is installed:
     ```bash
     sudo apt-get install nmap
     ```
   - Tool will automatically detect and use Nmap for scanning.
   - Manual use:
     ```bash
     nmap -p 1-1000 <target_ip>
     ```

**2. Vulnerability Database APIs:**
   - If integrating with an external vulnerability database (e.g., ExploitDB, NVD):
     - Add your API key to `config/config.yaml`:
       ```yaml
       vuln_db_api_key: "your-api-key-here"
       ```

**3. Automation/CI Integration:**
   - Using the tool in a CI/CD pipeline for automated security scans:
     - Add the following script to `.gitlab-ci.yml` or `Jenkinsfile`:
       ```bash
       python CLI.py --target $CI_COMMIT_REF --report json
       ```

**4. Logging and Results Export:**
   - Export results in various formats (JSON, HTML, PDF):
     ```bash
     python CLI.py --target <IP> --output json --output-file results.json
     ```

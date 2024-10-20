#### **Setup and Installation**

**1. Prerequisites:**
   - Python 3.8+
   - pip (Python package installer)
   - Git
   - Any external tools (e.g., Nmap for scanning)

**2. Installation Steps:**
   - Clone the repository:
     ```bash
     git clone https://github.com/mawg0ud/VulnVortex.git
     cd VulnVortex
     ```
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - Install additional external tools if needed:
     ```bash
     sudo apt install nmap
     ```

**3. Configuration:**
   - Adjust configurations in `config/config.yaml` for scanning settings, API keys, or directories.
   - Example configuration:
     ```yaml
     scan_settings:
       timeout: 5
       retries: 3
     ```

**4. Running the Tool:**
   - CLI usage:
     ```bash
     python CLI.py --target <IP> --ports <1-65535>
     ```

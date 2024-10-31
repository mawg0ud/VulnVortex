# VulnVortex - Advanced Network Vulnerability Scanner

![Version](https://img.shields.io/badge/version-1.0-blue.svg) ![License](https://img.shields.io/badge/license-MIT-green) ![Status](https://img.shields.io/badge/status-active-brightgreen)

**VulnVortex** is a network vulnerability scanner designed for in-depth network analysis, exploitation simulation, and vulnerability reporting. It provides an extensible platform suitable for both beginners and advanced users, offering a CLI, GUI, modular plugin support, and automation capabilities.


This tool provides a versatile toolset for proactive network security management, with powerful scanning capabilities and extensibility via plugins. Whether you're a security researcher, IT administrator, or developer, VulnVortex enhances your vulnerability detection and response strategy, tailored to suit both small and large-scale network environments.

## Features

- **Comprehensive Network Scanning**: Configurable IP and port range scanning with detailed vulnerability detection.
- **Flexible Interfaces**: Use CLI or GUI based on preferences.
- **Modular Plugin System**: Customize by adding plugins for new vulnerability checks.
- **Automated Reporting and Alerts**: Create reports and send alerts via email or Slack.
- **Third-Party Integration**: Easily integrate with external vulnerability databases and APIs.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [CLI Mode](#cli-mode)
  - [GUI Mode](#gui-mode)
- [Reports and Alerts](#reports-and-alerts)
- [Plugin Development](#plugin-development)
- [Testing and Validation](#testing-and-validation)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## Installation

To set up **VulnVortex**, clone the repository and install the required dependencies:

```bash
git clone https://github.com/your-username/VulnVortex.git
cd VulnVortex
pip install -r requirements.txt
```

## Configuration

### Configuration File (`config/config.yaml`)

VulnVortex uses a configuration file (`config/config.yaml`) for setting network parameters, vulnerability database details, and API keys. **Edit** the YAML file to customize settings such as IP range, scan frequency, reporting formats, and third-party API integrations.

**Sample Configuration:**

```yaml
network:
  ip_range: "192.168.1.0/24"
  scan_ports: "22,80,443"
reporting:
  output_directory: "reports/"
  format: "html"
vulnerability_database:
  update_frequency: "weekly"
  source_url: "https://vuln-db.org/api"
api_keys:
  some_service: "YOUR_API_KEY"
```

### Schema Validation

To ensure that `config.yaml` is correctly structured, validation occurs using `config/schema.yaml`. This provides a reliable way to detect configuration errors and maintain compatibility.

## Usage

**VulnVortex** provides both **CLI** and **GUI** interfaces to allow flexibility in usage.

### CLI Mode

The CLI interface offers granular control over scanning, reporting, and configuration management. Run a basic scan with the following command:

```bash
python main.py --mode cli --scan 192.168.1.0/24 --output html
```

**CLI Options:**

- `--scan`: Specify the IP range to scan.
- `--output`: Choose output report format (e.g., `html`, `txt`).

### GUI Mode

The GUI offers an intuitive interface for users preferring graphical controls. Launch with:

```bash
python main.py --mode gui
```

The GUI supports network range input, real-time scan results, and options to save reports.

## Reports and Alerts

### Report Generation

Reports are generated in HTML or plain-text formats, summarizing vulnerabilities, affected hosts, and severity. Reports are saved in the `reports/` directory by default.

### Alert Management

Configured alerts (email or Slack) notify administrators immediately upon finding high-severity vulnerabilities. These settings can be customized in `config.yaml`:

```yaml
reporting:
  email_settings:
    enabled: true
    smtp_server: "smtp.example.com"
    smtp_port: 587
  slack_webhook: "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXX"
```

## Plugin Development

The `plugins/` directory allows users to extend VulnVortex by creating custom plugins for additional vulnerability checks. Example plugins, such as `sample_plugin.py`, demonstrate the structure and integration process.

**Sample Plugin Structure:**

```python
class SamplePlugin:
    def __init__(self, scanner):
        self.scanner = scanner

    def run(self):
        # Plugin logic here
```

**Creating a New Plugin**: Create a new file in `plugins/`, following the structure of `sample_plugin.py`, and initialize it in the main `Scanner` class to make it operational.

## Testing and Validation

Testing modules are located in `tests/`, containing both unit and integration tests.

To run all tests:

```bash
python -m unittest discover tests
```

**Test Coverage**: Tests cover functionality for configuration loading, scanning logic, reporting, and integration with APIs. We recommend running tests regularly to ensure stability, especially after modifying core modules or adding plugins.

## Documentation

- **User Guide**: [docs/user_guide.md](docs/user_guide.md) - Detailed setup, usage examples, and best practices.
- **Developer Guide**: [docs/developer_guide.md](docs/developer_guide.md) - Contributing, plugin development, and project structure.
- **API Reference**: [docs/api_reference.md](docs/api_reference.md) - Complete API documentation for core modules and utilities.

## Contributing

We welcome contributions to improve VulnVortex. To contribute, please fork the repository, create a branch, and submit a pull request. Make sure to review the **developer documentation** and adhere to coding standards outlined in `docs/developer_guide.md`.

## License

VulnVortex is licensed under the MIT License. See [LICENSE](LICENSE) for more details.



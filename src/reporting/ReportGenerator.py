import json
import logging
from abc import ABC, abstractmethod
from jinja2 import Template

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ReportFormat(ABC):
    """
    Abstract base class for different report formats.
    Each format will have its own method to generate the report.
    """
    @abstractmethod
    def generate(self, data):
        pass

class JSONReportFormat(ReportFormat):
    """
    Concrete implementation for generating a JSON formatted report.
    """
    def generate(self, data):
        logging.info("Generating JSON report")
        return json.dumps(data, indent=4)

class HTMLReportFormat(ReportFormat):
    """
    Concrete implementation for generating an HTML formatted report.
    Uses Jinja2 templates for flexible HTML formatting.
    """
    def __init__(self, template_file=None):
        # Optional template file path for custom HTML report layouts
        self.template_file = template_file
        self.default_template = """
        <html>
        <head><title>Vulnerability Report</title></head>
        <body>
            <h1>Vulnerability Report for {{ target }}</h1>
            <h2>Exploitation Results:</h2>
            <ul>
            {% for result in exploitation_results %}
                <li>
                    Exploit: {{ result.exploit_name }} <br>
                    Success: {{ result.success }} <br>
                    Output: <pre>{{ result.raw_output }}</pre>
                </li>
            {% endfor %}
            </ul>
        </body>
        </html>
        """
        
    def generate(self, data):
        logging.info("Generating HTML report")
        
        # If a custom template file is provided, load it, else use default
        if self.template_file:
            with open(self.template_file, 'r') as file:
                template_content = file.read()
        else:
            template_content = self.default_template
        
        template = Template(template_content)
        html_output = template.render(data)
        
        return html_output

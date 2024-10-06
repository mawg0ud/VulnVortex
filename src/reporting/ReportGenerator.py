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

class PDFReportFormat(ReportFormat):
    """
    Concrete implementation for generating a PDF formatted report.
    Uses external libraries like `fpdf` or `reportlab` for PDF generation.
    """
    def __init__(self):
        from fpdf import FPDF
        self.pdf = FPDF()

    def generate(self, data):
        logging.info("Generating PDF report")

        self.pdf.add_page()
        self.pdf.set_font("Arial", size=12)
        
        self.pdf.cell(200, 10, txt=f"Vulnerability Report for {data['target']}", ln=True, align='C')

        self.pdf.ln(10)  # Newline
        self.pdf.cell(200, 10, txt="Exploitation Results:", ln=True, align='L')
        self.pdf.ln(5)

        for result in data['exploitation_results']:
            self.pdf.multi_cell(0, 10, f"Exploit: {result['exploit_name']}")
            self.pdf.multi_cell(0, 10, f"Success: {result['success']}")
            self.pdf.multi_cell(0, 10, f"Output:\n{result['raw_output']}")
            self.pdf.ln(5)

        # Save PDF to a file or return as bytes
        self.pdf_output = self.pdf.output(dest='S').encode('latin1')
        return self.pdf_output

class TextReportFormat(ReportFormat):
    """
    Concrete implementation for generating a plain text formatted report.
    """
    def generate(self, data):
        logging.info("Generating plain text report")
        text_output = f"Vulnerability Report for {data['target']}\n"
        text_output += "Exploitation Results:\n"
        
        for result in data['exploitation_results']:
            text_output += f"Exploit: {result['exploit_name']}\n"
            text_output += f"Success: {result['success']}\n"
            text_output += f"Output:\n{result['raw_output']}\n"
            text_output += "-" * 40 + "\n"

        return text_output


class ReportGenerator:
    """
    ReportGenerator class that handles the generation of reports in different formats.
    It takes in the results from vulnerability scans, exploitation attempts, and can generate reports in JSON, HTML, PDF, or plain text.
    """
    def __init__(self, format_type, template_file=None):
        self.format_type = format_type.lower()
        self.template_file = template_file
        
        # Instantiate the appropriate format class
        if self.format_type == "json":
            self.formatter = JSONReportFormat()
        elif self.format_type == "html":
            self.formatter = HTMLReportFormat(template_file=template_file)
        elif self.format_type == "pdf":
            self.formatter = PDFReportFormat()
        elif self.format_type == "text":
            self.formatter = TextReportFormat()
        else:
            raise ValueError(f"Unsupported report format: {self.format_type}")

    def generate_report(self, data):
        """
        Generates the report in the specified format using the format instance.
        """
        logging.info(f"Generating report in {self.format_type} format")
        return self.formatter.generate(data)


# Example usage:

if __name__ == "__main__":
    # Sample data structure (usually this comes from the scan/exploitation results)
    data = {
        "target": "192.168.1.10",
        "exploitation_results": [
            {
                "exploit_name": "CVE-2021-34527",
                "success": True,
                "raw_output": "Exploit succeeded, shell obtained!"
            },
            {
                "exploit_name": "CUSTOM-001",
                "success": False,
                "raw_output": "Exploit failed due to network timeout"
            }
        ]
    }

    # Generate a JSON report
    generator = ReportGenerator(format_type="json")
    json_report = generator.generate_report(data)
    print(json_report)

    # Generate an HTML report
    generator = ReportGenerator(format_type="html")
    html_report = generator.generate_report(data)
    print(html_report)

    # Generate a PDF report (bytes)
    generator = ReportGenerator(format_type="pdf")
    pdf_report = generator.generate_report(data)
    
    # Save PDF to a file
    with open("vulnerability_report.pdf", "wb") as pdf_file:
        pdf_file.write(pdf_report)

    # Generate a plain text report
    generator = ReportGenerator(format_type="text")
    text_report = generator.generate_report(data)
    print(text_report)

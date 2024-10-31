import json
import csv
import os
from jinja2 import Template

class ScanReportConverter:
    def __init__(self, scan_file, output_format="html"):
        self.scan_file = scan_file
        self.output_format = output_format
        self.template_dir = "templates"
        
    def load_scan_file(self):
        """Load scan result from JSON file."""
        with open(self.scan_file, 'r') as f:
            return json.load(f)

    def convert_to_html(self, scan_data):
        """Convert scan data to HTML format using a template."""
        template_path = os.path.join(self.template_dir, 'scan_report.html')
        with open(template_path, 'r') as f:
            template = Template(f.read())
        html_content = template.render(scan_data=scan_data)
        
        output_file = self.scan_file.replace('.json', '.html')
        with open(output_file, 'w') as f:
            f.write(html_content)
        print(f"HTML report saved: {output_file}")
    
    def convert_to_csv(self, scan_data):
        """Convert scan data to CSV format."""
        csv_file = self.scan_file.replace('.json', '.csv')
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(scan_data[0].keys())  # Write header
            for entry in scan_data:
                writer.writerow(entry.values())
        print(f"CSV report saved: {csv_file}")

    def run_conversion(self):
        """Runs the appropriate conversion based on the format."""
        scan_data = self.load_scan_file()

        if self.output_format == "html":
            self.convert_to_html(scan_data)
        elif self.output_format == "csv":
            self.convert_to_csv(scan_data)
        else:
            print(f"Unsupported format: {self.output_format}")

if __name__ == "__main__":
    converter = ScanReportConverter("results/scan_results.json", output_format="html")
    converter.run_conversion()

import unittest
import json
from ReportGenerator import ReportGenerator

class TestReportGenerator(unittest.TestCase):

    def setUp(self):
        """Set up data for report generation."""
        with open("valid_exploit_results.json", "r") as f:
            self.results = json.load(f)

    def test_generate_json_report(self):
        """Test generating a report in JSON format."""
        generator = ReportGenerator(format_type="json")
        report = generator.generate_report(self.results)
        self.assertIsInstance(report, str, "JSON report should be a string")
        json_report = json.loads(report)
        self.assertIn("vulnerabilities", json_report, "JSON report must contain a vulnerabilities section")
    
    def test_generate_html_report(self):
        """Test generating a report in HTML format."""
        generator = ReportGenerator(format_type="html")
        report = generator.generate_report(self.results)
        self.assertIn("<html>", report, "HTML report should contain an <html> tag")
        self.assertIn("</html>", report, "HTML report should contain a closing </html> tag")

    def test_generate_pdf_report(self):
        """Test generating a report in PDF format."""
        generator = ReportGenerator(format_type="pdf")
        report = generator.generate_report(self.results)
        self.assertIsInstance(report, bytes, "PDF report should be in bytes format")
    
    def test_invalid_format(self):
        """Test handling of invalid format type."""
        with self.assertRaises(ValueError):
            generator = ReportGenerator(format_type="invalid_format")
            generator.generate_report(self.results)

if __name__ == '__main__':
    unittest.main()

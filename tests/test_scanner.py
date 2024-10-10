import unittest
from Scanner import Scanner

class TestScanner(unittest.TestCase):
    
    def test_scan_single_port(self):
        """Test scanning a single port."""
        scanner = Scanner("192.168.1.1", "80")
        result = scanner.perform_scan()
        self.assertIn("80", result, "Port 80 should be included in the scan results")

    def test_scan_port_range(self):
        """Test scanning a range of ports."""
        scanner = Scanner("192.168.1.1", "22-80")
        result = scanner.perform_scan()
        self.assertIn("22", result, "Port 22 should be included in the scan results")
        self.assertIn("80", result, "Port 80 should be included in the scan results")

    def test_invalid_ip_address(self):
        """Test handling of invalid IP address."""
        scanner = Scanner("999.999.999.999", "80")
        with self.assertRaises(ValueError):
            scanner.perform_scan()

    def test_invalid_port_range(self):
        """Test handling of invalid port range."""
        scanner = Scanner("192.168.1.1", "99999")
        with self.assertRaises(ValueError):
            scanner.perform_scan()

    def test_scan_output_format(self):
        """Test if the output format is correct."""
        scanner = Scanner("192.168.1.1", "80")
        result = scanner.perform_scan()
        self.assertIsInstance(result, str, "Scan result should be a string")

if __name__ == '__main__':
    unittest.main()

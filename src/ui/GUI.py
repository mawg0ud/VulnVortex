import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import json
import os

from Scanner import Scanner
from VulnerabilityScanner import VulnerabilityScanner
from Exploitation import ExploitManager
from ReportGenerator import ReportGenerator


class VulnerabilityScannerGUI:
    """
    Main class for the vulnerability scanner GUI application using tkinter.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("VulnVortex - Vulnerability Scanner and Exploitation Tool")
        self.root.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        """
        Create all widgets for the main window.
        """
        # Notebook (Tab control)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        # Scan Tab
        self.scan_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.scan_tab, text='Scan')

        # Vulnerability Scan Tab
        self.vuln_scan_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.vuln_scan_tab, text='Vulnerability Scan')

        # Exploit Tab
        self.exploit_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.exploit_tab, text='Exploit')

        # Report Tab
        self.report_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.report_tab, text='Generate Report')

        # Initialize each tab
        self.init_scan_tab()
        self.init_vuln_scan_tab()
        self.init_exploit_tab()
        self.init_report_tab()

    def init_scan_tab(self):
        """
        Initialize the Scan tab components.
        """
        label = ttk.Label(self.scan_tab, text="Scan for open ports and services", font=("Helvetica", 14))
        label.pack(pady=10)

        self.target_entry = ttk.Entry(self.scan_tab, width=50)
        self.target_entry.pack(pady=5)
        self.target_entry.insert(0, "Target IP or Host")

        self.port_entry = ttk.Entry(self.scan_tab, width=50)
        self.port_entry.pack(pady=5)
        self.port_entry.insert(0, "Ports (e.g., 1-65535)")

        scan_button = ttk.Button(self.scan_tab, text="Start Scan", command=self.start_scan)
        scan_button.pack(pady=10)

        self.scan_result_text = tk.Text(self.scan_tab, wrap=tk.WORD, height=15)
        self.scan_result_text.pack(pady=10)

    def init_vuln_scan_tab(self):
        """
        Initialize the Vulnerability Scan tab components.
        """
        label = ttk.Label(self.vuln_scan_tab, text="Scan for vulnerabilities", font=("Helvetica", 14))
        label.pack(pady=10)

        self.vuln_target_entry = ttk.Entry(self.vuln_scan_tab, width=50)
        self.vuln_target_entry.pack(pady=5)
        self.vuln_target_entry.insert(0, "Target IP or Host")

        self.scan_file_button = ttk.Button(self.vuln_scan_tab, text="Load Scan Results", command=self.load_scan_file)
        self.scan_file_button.pack(pady=5)

        self.vuln_scan_result_text = tk.Text(self.vuln_scan_tab, wrap=tk.WORD, height=15)
        self.vuln_scan_result_text.pack(pady=10)

        vuln_scan_button = ttk.Button(self.vuln_scan_tab, text="Start Vulnerability Scan", command=self.start_vuln_scan)
        vuln_scan_button.pack(pady=10)

    def init_exploit_tab(self):
        """
        Initialize the Exploit tab components.
        """
        label = ttk.Label(self.exploit_tab, text="Exploit vulnerabilities", font=("Helvetica", 14))
        label.pack(pady=10)

        self.exploit_target_entry = ttk.Entry(self.exploit_tab, width=50)
        self.exploit_target_entry.pack(pady=5)
        self.exploit_target_entry.insert(0, "Target IP or Host")

        self.vulns_file_button = ttk.Button(self.exploit_tab, text="Load Vulnerabilities File", command=self.load_vulns_file)
        self.vulns_file_button.pack(pady=5)

        self.exploit_result_text = tk.Text(self.exploit_tab, wrap=tk.WORD, height=15)
        self.exploit_result_text.pack(pady=10)

        exploit_button = ttk.Button(self.exploit_tab, text="Start Exploitation", command=self.start_exploit)
        exploit_button.pack(pady=10)

    def init_report_tab(self):
        """
        Initialize the Report tab components.
        """
        label = ttk.Label(self.report_tab, text="Generate exploitation report", font=("Helvetica", 14))
        label.pack(pady=10)

        self.report_target_entry = ttk.Entry(self.report_tab, width=50)
        self.report_target_entry.pack(pady=5)
        self.report_target_entry.insert(0, "Target IP or Host")

        self.results_file_button = ttk.Button(self.report_tab, text="Load Exploit Results", command=self.load_results_file)
        self.results_file_button.pack(pady=5)

        self.format_combobox = ttk.Combobox(self.report_tab, values=["json", "html", "pdf", "text"], state="readonly")
        self.format_combobox.pack(pady=5)
        self.format_combobox.set("Select Report Format")

        report_button = ttk.Button(self.report_tab, text="Generate Report", command=self.generate_report)
        report_button.pack(pady=10)

        self.report_result_text = tk.Text(self.report_tab, wrap=tk.WORD, height=15)
        self.report_result_text.pack(pady=10)

    def start_scan(self):
        """
        Starts the scan on a separate thread.
        """
        target = self.target_entry.get()
        ports = self.port_entry.get()
        if not target or not ports:
            messagebox.showwarning("Input Error", "Please enter a target and ports.")
            return

        self.scan_result_text.delete(1.0, tk.END)
        threading.Thread(target=self.run_scan, args=(target, ports)).start()

    def run_scan(self, target, ports):
        """
        Perform the scan and update the result in the GUI.
        """
        scanner = Scanner(target, ports)
        results = scanner.perform_scan()
        self.scan_result_text.insert(tk.END, results)

    def start_vuln_scan(self):
        """
        Starts the vulnerability scan on a separate thread.
        """
        target = self.vuln_target_entry.get()
        if not target or not hasattr(self, 'scan_result_file'):
            messagebox.showwarning("Input Error", "Please select a target and load scan results.")
            return

        self.vuln_scan_result_text.delete(1.0, tk.END)
        threading.Thread(target=self.run_vuln_scan, args=(target, self.scan_result_file)).start()



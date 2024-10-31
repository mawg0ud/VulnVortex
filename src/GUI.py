import tkinter as tk
from tkinter import messagebox, filedialog
from src.core.Scanner import Scanner
from src.utils.ConfigManager import ConfigManager
from src.core.ReportGenerator import ReportGenerator

class GUI:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.scanner = Scanner(self.config_manager.config)
        self.root = tk.Tk()
        self.root.title("Vulnerability Scanner GUI")
        self.setup_gui()

    def setup_gui(self):
        tk.Label(self.root, text="Network Range:").grid(row=0, column=0, padx=10, pady=5)
        self.network_entry = tk.Entry(self.root, width=30)
        self.network_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Button(self.root, text="Run Scan", command=self.run_scan).grid(row=1, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit).grid(row=2, column=0, columnspan=2, pady=5)

    def run_scan(self):
        network_range = self.network_entry.get()
        if not network_range:
            messagebox.showwarning("Input Required", "Please enter a network range to scan.")
            return
        
        vulnerabilities = self.scanner.scan_network(network_range)
        if vulnerabilities:
            messagebox.showinfo("Scan Complete", f"Found {len(vulnerabilities)} vulnerabilities.")
            save_path = filedialog.asksaveasfilename(defaultextension=".html",
                                                     filetypes=[("HTML files", "*.html"), ("Text files", "*.txt")])
            if save_path:
                report_gen = ReportGenerator(output_format="html")
                report_gen.generate(vulnerabilities, save_path)
                messagebox.showinfo("Report Saved", f"Report saved at {save_path}.")
        else:
            messagebox.showinfo("Scan Complete", "No vulnerabilities found.")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = GUI()
    gui.run()

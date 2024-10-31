import smtplib
import json
import requests
from email.mime.text import MIMEText

class AlertManager:
    def __init__(self, config_file="config/config.json"):
        self.config = self.load_config(config_file)
        self.email_settings = self.config["reporting"]["email_settings"]
        self.slack_webhook = self.config["notifications"]["slack_webhook"]

    def load_config(self, config_file):
        """Loads configuration settings from a JSON file."""
        with open(config_file, 'r') as f:
            return json.load(f)

    def send_email_alert(self, subject, message):
        """Sends an email alert."""
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = self.email_settings['email_from']
        msg['To'] = self.email_settings['email_to']
        
        try:
            with smtplib.SMTP(self.email_settings['smtp_server'], self.email_settings['smtp_port']) as server:
                server.sendmail(self.email_settings['email_from'], self.email_settings['email_to'], msg.as_string())
                print("Email alert sent successfully.")
        except Exception as e:
            print(f"Failed to send email alert: {str(e)}")

    def send_slack_alert(self, message):
        """Sends an alert via Slack."""
        data = {'text': message}
        response = requests.post(self.slack_webhook, json=data)
        if response.status_code == 200:
            print("Slack alert sent successfully.")
        else:
            print(f"Failed to send Slack alert: {response.status_code}")

if __name__ == "__main__":
    alert_manager = AlertManager()
    alert_manager.send_email_alert("Critical Vulnerability Detected", "Details of the vulnerability...")
    alert_manager.send_slack_alert("Critical Vulnerability Detected")

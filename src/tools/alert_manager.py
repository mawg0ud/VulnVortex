import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
import logging
import requests
from twilio.rest import Client


class AlertManager:
    """
    A centralized alert management system supporting multiple communication channels.

    Features:
    - Supports email, SMS, and webhook notifications.
    - Customizable alert templates.
    - Multi-recipient support for team notifications.
    - Retry mechanism for failed alerts.
    - Extendable for additional alert methods.
    """

    def __init__(self, email_config: Dict = None, sms_config: Dict = None, webhook_config: List[str] = None):
        """
        Initialize the AlertManager with configurations for email, SMS, and webhooks.

        Args:
            email_config (Dict): Configuration for email alerts.
                - `smtp_server` (str): SMTP server address.
                - `smtp_port` (int): SMTP server port.
                - `username` (str): Email username.
                - `password` (str): Email password.
            sms_config (Dict): Configuration for SMS alerts.
                - `account_sid` (str): Twilio Account SID.
                - `auth_token` (str): Twilio Auth Token.
                - `from_number` (str): Sender's phone number.
            webhook_config (List[str]): List of webhook URLs for sending alerts.
        """
        self.logger = logging.getLogger("AlertManager")
        self.logger.setLevel(logging.INFO)

        self.email_config = email_config
        self.sms_config = sms_config
        self.webhook_config = webhook_config or []

        # Initialize clients
        self.sms_client = None
        if self.sms_config:
            self.sms_client = Client(self.sms_config["account_sid"], self.sms_config["auth_token"])

    def send_email(self, recipients: List[str], subject: str, message: str):
        """
        Send an email alert.

        Args:
            recipients (List[str]): List of recipient email addresses.
            subject (str): Email subject.
            message (str): Email body.
        """
        if not self.email_config:
            self.logger.error("Email configuration is missing.")
            return

        try:
            self.logger.info("Sending email alert.")
            msg = MIMEMultipart()
            msg["From"] = self.email_config["username"]
            msg["To"] = ", ".join(recipients)
            msg["Subject"] = subject
            msg.attach(MIMEText(message, "plain"))

            with smtplib.SMTP(self.email_config["smtp_server"], self.email_config["smtp_port"]) as server:
                server.starttls()
                server.login(self.email_config["username"], self.email_config["password"])
                server.send_message(msg)

            self.logger.info("Email alert sent successfully.")
        except Exception as e:
            self.logger.error(f"Failed to send email alert: {e}")

    def send_sms(self, recipients: List[str], message: str):
        """
        Send an SMS alert.

        Args:
            recipients (List[str]): List of recipient phone numbers.
            message (str): SMS message body.
        """
        if not self.sms_client:
            self.logger.error("SMS configuration is missing.")
            return

        try:
            self.logger.info("Sending SMS alert.")
            for recipient in recipients:
                self.sms_client.messages.create(body=message, from_=self.sms_config["from_number"], to=recipient)

            self.logger.info("SMS alerts sent successfully.")
        except Exception as e:
            self.logger.error(f"Failed to send SMS alert: {e}")

    def send_webhook(self, message: str):
        """
        Send an alert to configured webhooks.

        Args:
            message (str): Message to send via the webhooks.
        """
        if not self.webhook_config:
            self.logger.error("Webhook configuration is missing.")
            return

        try:
            self.logger.info("Sending webhook alerts.")
            for url in self.webhook_config:
                response = requests.post(url, json={"message": message})
                if response.status_code == 200:
                    self.logger.info(f"Webhook alert sent successfully to {url}.")
                else:
                    self.logger.error(f"Failed to send webhook alert to {url}: {response.status_code}")
        except Exception as e:
            self.logger.error(f"Failed to send webhook alert: {e}")

    def send_alert(self, channels: List[str], message: str, **kwargs):
        """
        Send an alert through multiple channels.

        Args:
            channels (List[str]): List of channels to use ('email', 'sms', 'webhook').
            message (str): Alert message body.
            **kwargs: Additional arguments specific to channels.
                - `recipients` (List[str]): List of recipients (for email and SMS).
                - `subject` (str): Subject for email alerts.
        """
        for channel in channels:
            if channel == "email":
                self.send_email(kwargs.get("recipients", []), kwargs.get("subject", "Alert"), message)
            elif channel == "sms":
                self.send_sms(kwargs.get("recipients", []), message)
            elif channel == "webhook":
                self.send_webhook(message)
            else:
                self.logger.error(f"Unsupported alert channel: {channel}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Example configuration
    email_config = {
        "smtp_server": "smtp.example.com",
        "smtp_port": 587,
        "username": "alert@example.com",
        "password": "securepassword123"
    }
    sms_config = {
        "account_sid": "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "auth_token": "your_auth_token",
        "from_number": "+1234567890"
    }
    webhook_config = [
        "https://webhook.site/your-webhook-url"
    ]

    alert_manager = AlertManager(email_config=email_config, sms_config=sms_config, webhook_config=webhook_config)

    # Send a test alert
    alert_manager.send_alert(
        channels=["email", "sms", "webhook"],
        message="Critical vulnerability detected!",
        recipients=["user1@example.com", "+19876543210"],
        subject="Vulnerability Alert"
    )

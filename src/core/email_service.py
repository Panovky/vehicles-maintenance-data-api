import os
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from imapclient import imap_utf7


class EmailService:
    def __init__(self):
        self.sender_address = os.getenv('EMAIL_ADDRESS')
        self.sender_app_password = os.getenv('EMAIL_APP_PASSWORD')
        self.sender_smtp_server = os.getenv('EMAIL_SMTP_SERVER')
        self.sender_imap_server = os.getenv('EMAIL_IMAP_SERVER')
        self.sender_smtp_port = int(os.getenv('EMAIL_SMTP_PORT'))
        self.sender_imap_port = int(os.getenv('EMAIL_IMAP_PORT'))

    def send_email(self, receiver_address, subject, text, html):
        message = MIMEMultipart('alternative')
        message['From'] = self.sender_address
        message['To'] = receiver_address
        message['Subject'] = Header(subject, 'utf-8')

        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        message.attach(part1)
        message.attach(part2)

        smtp = smtplib.SMTP_SSL(self.sender_smtp_server, self.sender_smtp_port)
        smtp.login(self.sender_address, self.sender_app_password)
        smtp.sendmail(self.sender_address, receiver_address, message.as_string())
        smtp.quit()

        imap = imaplib.IMAP4_SSL(self.sender_imap_server, self.sender_imap_port)
        imap.login(self.sender_address, self.sender_app_password)
        imap.append(
            mailbox=str(imap_utf7.encode('Отправленные'))[2:-1],
            flags=None,
            date_time=None,
            message=message.as_bytes())
        imap.logout()

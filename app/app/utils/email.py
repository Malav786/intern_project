from fastapi import FastAPI
from fastapi import APIRouter, Depends
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from email.message import EmailMessage
from email_validator import validate_email, EmailNotValidError


class email():
    def send_email(to: str, subject: int):
        sender_email = "20it013@charusat.edu.in"
        sender_password = "tovkxltsnjxfrhhs"
        msg = EmailMessage()
        msg['Subject'] = "OTP"
        msg['From'] = sender_email
        msg['To'] = to
        msg.set_content(
            f"""\
            Otp : {subject}
            """,
        )
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        return True
        


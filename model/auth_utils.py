from email.mime.text import MIMEText
import smtplib
from os import environ

def send_email(to_addr: str, code: int) -> bool:
    msg = MIMEText(f"Your login code is {code}")
    msg["Subject"] = "Login Code"
    msg["From"] = "no-reply@pm.gmail.com"
    msg["To"] = to_addr
    #try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(environ["PM_SMTP_USERNAME"], environ["PM_SMTP_PASSWORD"])
        server.send_message(msg)
        return True
    #except smtplib.SMTPException:
        #print("Email not sent!")
        #return False
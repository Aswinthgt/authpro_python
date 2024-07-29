import smtplib
from pydantic import EmailStr, BaseModel
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


class EmailSchema(BaseModel):
    email: EmailStr
    subject: str
    message: str


def send_mail(email: EmailSchema):
    msg = MIMEMultipart()
    msg["From"] = os.getenv("MAIL")
    msg["To"] = email.email
    msg["Subject"] = email.subject

    msg.attach(MIMEText(email.message, "plain"))
    try:
        server = smtplib.SMTP("smtp.office365.com", 587)
        server.starttls()
        server.login(os.getenv("MAIL"), os.getenv("MAIL_PASS"))
        server.sendmail(os.getenv("MAIL"), email.email, msg.as_string())
        server.close()
        return True
    except Exception as e:
        print(e)
        return False

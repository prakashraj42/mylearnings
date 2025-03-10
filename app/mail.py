from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
import os
from jinja2 import Template
from pathlib import Path

# Load environment variables
load_dotenv()

TEMPLATE_FOLDER = Path(__file__).parent / "mail-template"
print(TEMPLATE_FOLDER)

# Ensure values are not None
MAIL_USERNAME = os.getenv("EMAIL_USERNAME")
MAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")

if not MAIL_USERNAME or not MAIL_PASSWORD or not MAIL_FROM:
    raise ValueError("Missing environment variables: EMAIL_USERNAME, EMAIL_PASSWORD, MAIL_FROM")

# Configure your mail settings
conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=587,  # Use 587 for TLS (Recommended)
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,  # Corrected field
    MAIL_SSL_TLS=False,  # Corrected field
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER=TEMPLATE_FOLDER
)

# Define the email schema
class EmailSchema(BaseModel):
    email: EmailStr
    subject: str
    body: str



async def send_registration_email(email: EmailStr, name: str, role: str):
    """Send registration email with user details"""
    
    # Load and render the template
    template_path = TEMPLATE_FOLDER / "otp_send.html"
    
    if not template_path.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")

    with open(template_path, "r", encoding="utf-8") as file:
        template = Template(file.read())
    
    html_content = template.render(name=name, email=email, role=role)

    message = MessageSchema(
        subject="Welcome to Our Platform!",
        recipients=[email],  
        body=html_content,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)

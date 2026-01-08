#LIBRARIES
import smtplib
from email.message import EmailMessage
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

def send_simple_email(to: str, subject: str, html_content: str) -> None:
    

    message = EmailMessage()
    message["From"] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
    message["To"] = to
    message["Subject"] = subject

    # Set HTML content
    message.set_content("This email requires an HTML-compatible email client.")
    message.add_alternative(html_content, subtype="html")

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            # Secure the connection if possible
            try:
                server.starttls()
            except Exception:
                logger.info("SMTP server does not support STARTTLS")

            # Authenticate if credentials are provided
            if settings.SMTP_USER and settings.SMTP_PASSWORD:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)

            server.send_message(message)

    except Exception as e:
        logger.error(f"Failed to send email to {to}: {e}")

def send_verification_email(user_email: str, token: str) -> None:
   
    html_content = f"""
    <html>
        <body>
            <p>Please verify your email by clicking the link below:</p>
            <a href="{settings.API_V1_STR}/auth/verify-email?token={token}">Verify Email</a>
        </body>
    </html>
    """
    send_simple_email(to=user_email, subject="Verify your email for Continuum", html_content=html_content)
    

def send_password_reset_email(user_email: str, token: str):
    
    html_content = f"""
    <html>
        <body>
            <p>Reset your password by clicking the link below:</p>
            <a href="{settings.API_V1_STR}/auth/reset-password?token={token}">Reset Password</a>
        </body>
    </html>
    """
    send_simple_email(to=user_email, subject="Password Reset Request", html_content=html_content)
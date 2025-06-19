
from typing import List, Any
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from pydantic import EmailStr
from datetime import  datetime
from ..core.config import setting
from pathlib import Path
from jinja2 import Template
from dataclasses import dataclass


@dataclass
class EmailData:
  html_content: str
  subject: str


mail_config = ConnectionConfig(
  MAIL_USERNAME= setting.SMTP_USER,
  MAIL_PASSWORD= setting.SMTP_PASSWORD,
  MAIL_FROM= setting.EMAILS_FROM_EMAIL,
  MAIL_PORT= 587,
  MAIL_SERVER = setting.SMTP_HOST,
  MAIL_FROM_NAME =  "Monix",#setting.MAIL_FROM_NAME,
  MAIL_STARTTLS = True,
  MAIL_SSL_TLS = False,
  USE_CREDENTIALS = True,
  VALIDATE_CERTS = True,
)



mail = FastMail(
  config= mail_config
)



def render_email_template(*, template_name: str, context: dict[str, Any]) -> str:
  template_str = (
      Path(__file__).parent / "build" / template_name
  ).read_text()

  html_content = Template(template_str).render(context)
  return html_content


def create_message(recipients: List[EmailStr], subject: str, body: str):
  message = MessageSchema(
    subject=subject,
    recipients=recipients,
    body=body,
    subtype=MessageType.html
  )
  return message



async def generate_new_account_email(
    email_to: EmailStr, username: str, verify_token:str
) :
  project_name = setting.PROJECT_NAME
  subject = f"{project_name} - New account for user {username}"
  html_content = render_email_template(
    template_name="verify.html",
    context={
      "project_name": setting.PROJECT_NAME,
      "username": username,
      "email": email_to,
      "link": f'http://{setting.SERVER_DOMAIN}:{setting.SERVER_PORT}/email-verify?token={verify_token}', #! f'{setting.FRONTEND_HOST}/email-verify?token={verify_token}'
      "logo_url": "https://logowik.com/content/uploads/images/fastapi6230.logowik.com.webp",
      "loc_url": "https://img.favpng.com/12/18/7/emoji-lock-sms-text-messaging-clip-art-png-favpng-VbztJs45heqffjrhJuhaSYXhV.jpg",
      "support_link": "https://example.com/support",
      "exp": setting.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
      "year": datetime.now().year,
    },
  )
  message = create_message([email_to], subject,html_content )

  await mail.send_message(message)






















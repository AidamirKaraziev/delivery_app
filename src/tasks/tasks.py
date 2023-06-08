import smtplib
from email.message import EmailMessage
from typing import Optional

from celery import Celery

from config import SMTP_USER, SMTP_PASSWORD

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery('tasks', broker='redis://localhost:6379')


def get_email_template_forgot_password(name: str, email_to: Optional[str], token: str):
    email = EmailMessage()
    email['Subject'] = 'Токен для смены пароля'
    email['From'] = SMTP_USER
    email['TO'] = email_to

    email.set_content(
        '<div>'
        f'<h1 style="color: red;">Здравствуйте, {name}, а вот и ваш токен. Зацените 😊</h1>'
        f'<h2 style="color: blue;">{token}</h2>'
        '<img src="https://avatars.mds.yandex.net/i?id=08dfbbeb4c849fb816c77a5b03a880612bf491c3-8257511-images-thumbs&n=13'
        '-management-dashboard-ui-design-template-suitable-designing-application-for-android-and-ios-clean-style-app'
        '-mobile-free-vector.jpg" width="600">'
        '</div>',
        subtype='html'
    )

    return email


@celery.task
def send_email_report_forgot_password(token: str, name: str, email_to: str):
    email = get_email_template_forgot_password(token=token, name=name, email_to=email_to)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)

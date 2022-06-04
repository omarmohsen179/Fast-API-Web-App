import os
from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from App.models import schemas
from dotenv import load_dotenv


class Envs:
    MAIL_USERNAME = "omar179771@bue.edu.eg"
    MAIL_PASSWORD = "Code010066@1"
    MAIL_FROM = "omar179771@bue.edu.eg"
    MAIL_PORT = 587
    MAIL_SERVER = "smtp.office365.com"
    MAIL_FROM_NAME = "omar179771@bue.edu.eg"

    """MAIL_SERVER="smtp.gmail.com",
    MAIL_USERNAME="mohsenomar350@gmail.com",
    MAIL_FROM="mohsenomar350@gmail.com",
    MAIL_FROM_NAME="MAIL_FROM_NAME",
    MAIL_PASSWORD="Thanks010066@","""


conf = ConnectionConfig(
    MAIL_USERNAME=Envs.MAIL_USERNAME,
    MAIL_PASSWORD=Envs.MAIL_PASSWORD,
    MAIL_FROM=Envs.MAIL_FROM,
    MAIL_PORT=Envs.MAIL_PORT,
    MAIL_SERVER=Envs.MAIL_SERVER,
    MAIL_FROM_NAME=Envs.MAIL_FROM_NAME,
    MAIL_SSL=False,
    MAIL_TLS=True,
    TEMPLATE_FOLDER='./templates'

)


async def send_email_async(subject: str, email_to: str, body: schemas.template_body):

    body.helpLink = "support.com"
    body.unsubscribeMail = "unsupport.com"
    message = MessageSchema(
        subject=subject,
        recipients=email_to,
        subtype='html',
        template_body=body,

    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name='email.html')


def send_email_background(background_tasks: BackgroundTasks, subject: str, email_to: str, body: schemas.template_body):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=body,
        subtype='html',

    )

    fm = FastMail(conf)

    background_tasks.add_task(
        fm.send_message, message, template_name='email.html')

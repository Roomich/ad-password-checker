import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from dotenv import load_dotenv


def send_email(text, mail_server, server_port,
    login, password, filename, to, subject,
):
    message = MIMEMultipart()
    message['From'] = login
    message['To'] = to
    message['Subject'] = subject
    message.attach(MIMEText(text, 'plain'))

    with open(filename, 'rb') as file:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f"attachment; filename={filename}"
        )

    message.attach(part)

    with smtplib.SMTP(mail_server, server_port) as smtpObj:
        smtpObj.starttls()
        smtpObj.login(login, password)
        try:
            smtpObj.send_message(message)
        finally:
            smtpObj.quit()


if __name__ == '__main__':
    
    load_dotenv()
    
    filename = 'filename.xlsx'
    mail_server = os.getenv('MAIL_SERVER', '')
    login = os.getenv('MAIL_LOGIN', '')
    password = os.getenv('MAIL_PASS', '')
    server_port = os.getenv('MAIL_SERVER_PORT', '')
    to = 'roman.odinichenko@nces.by'
    subject = 'Учётные записи с истекающим сроком действия пароля'
    text = '''
Hello my friend!
This is a test message!
Do not respond it!
'''

    send_email(text, mail_server, server_port,
        login, password, filename, to, subject,
    )

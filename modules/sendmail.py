import smtplib
import os

from dotenv import load_dotenv

load_dotenv()

mail_server = os.getenv('MAIL_SERVER', '')
login = os.getenv('MAIL_LOGIN', '')
password = os.getenv('MAIL_PASS', '')
server_port = 587

tolist=['your@mail.any']

msg='''\
From: PasswordChecker
Subject: Duck

hello my friend!
this is a test message!
Do not respond it!
'''
with smtplib.SMTP(mail_server, server_port) as smtpObj:
    smtpObj.starttls()
    smtpObj.login(login, password)
    try:
        smtpObj.sendmail(login, tolist, msg)
    finally:
        smtpObj.quit()
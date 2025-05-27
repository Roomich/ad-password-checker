import os

from ldap3 import Server, Connection
from dotenv import load_dotenv

from modules.sendmail import send_email
from modules.functions import (
    get_pass_lifetime_left,
    sort_users,
    export_to_excel
)

load_dotenv()

SERVER = os.getenv('SERVER', '')
USER = os.getenv('DISTINGUISHED_NAME', '')
PASSWORD = os.getenv('PASSWORD', '')
PASSWORD_TTL = int(os.getenv('PASSWORD_TTL', ''))
START_ALARM_PERIOD = int(os.getenv('START_ALARM_PERIOD', ''))

server = Server(SERVER, use_ssl=True)


@sort_users(START_ALARM_PERIOD)
def get_users_list():

    with Connection(server, USER, PASSWORD, auto_bind=True) as conn:

        conn.search(
            'dc=main,dc=nces,dc=by',
            '(&(description=*ОССТИ*)(objectClass=user))',
            attributes=['cn', 'pwdLastSet', 'userAccountControl']
        )

        result = [
            {
                'name': entry.cn.values[0],
                'daysLeft': get_pass_lifetime_left(
                    PASSWORD_TTL,
                    str(entry['pwdLastSet'])
                ),
                'acccountCode': entry.userAccountControl[0]
            } for entry in conn.entries
        ]

    return result


def main():
    data = get_users_list()
    if data:
        filename = export_to_excel(data)
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
    os.remove('filename.xlsx')


if __name__ == '__main__':
    main()

import os

from ldap3 import Server, Connection
from dotenv import load_dotenv

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
            attributes=['cn', 'pwdLastSet']
        )

        result = [
            {
                'name': entry.cn.values[0],
                'days_left': get_pass_lifetime_left(
                    PASSWORD_TTL,
                    str(entry['pwdLastSet'])
                )
            } for entry in conn.entries
        ]

    return result


def main():
    data = get_users_list()
    if data:
        export_to_excel(data)
    # os.remove('filename.xlsx')


if __name__ == '__main__':
    main()

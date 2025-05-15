import os

from ldap3 import Server, Connection
from dotenv import load_dotenv

from modules.functions import get_pass_lifetime_left

load_dotenv()

SERVER = os.getenv('SERVER', '')
USER = os.getenv('DISTINGUISHED_NAME', '')
PASSWORD = os.getenv('PASSWORD', '')
PASSWORD_TTL = int(os.getenv('PASSWORD_TTL', ''))
START_ALARM_PERIOD = int(os.getenv('START_ALARM_PERIOD', ''))

server = Server(SERVER, use_ssl=True)


def get_users_list():

    with Connection(server, USER, PASSWORD, auto_bind=True) as conn:

        conn.search(
            'dc=main,dc=nces,dc=by',
            '(description=*[tech]*)',
            attributes=['cn', 'pwdLastSet']
        )

        get_str_datetime = lambda x: x.split('.')[0] if isinstance(x, str) else None

        result = [
            {
                'name' : entry.cn.values[0],
                'days_left': get_pass_lifetime_left(
                    PASSWORD_TTL,
                    get_str_datetime(str(entry['pwdLastSet']))
                )
            } for entry in conn.entries
        ]

    return result


if __name__ == '__main__':
    print(get_users_list())
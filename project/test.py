from datetime import datetime, timedelta


def get_pass_lifetime_left(pass_lifetime, str_date):
    
    delta = timedelta(days=pass_lifetime)    
    format = '%Y-%m-%d %H:%M:%S'    

    pass_changed = datetime.strptime(str_date, format)
    today = datetime.today()

    days_left = (pass_changed + delta - today).days

    return days_left


if __name__ == '__main__':
    PASSWORD_LIFETIME = 90
    str_date = '2025-05-07 14:06:12'
    print(get_pass_lifetime_left(PASSWORD_LIFETIME, str_date))

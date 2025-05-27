from datetime import datetime, timedelta
import smtplib

import pandas as pd


def get_pass_lifetime_left(pass_lifetime, str_date):

    if '.' not in str_date:
        str_date = str_date.split('+')[0]
    else:
        str_date = str_date.split('.')[0]

    delta = timedelta(days=pass_lifetime)
    format = '%Y-%m-%d %H:%M:%S'

    pass_changed = datetime.strptime(str_date, format)
    today = datetime.today()

    days_left = (pass_changed + delta - today).days

    return days_left


# Code 66050 - user is blocked
# Code 66048 - password never expires
# Code 512 - normal user
def sort_users(parameter):
    def get_function(function):
        def wrapper(*args, **kwargs):
            result = function()
            return [
                i for i in result
                if i['daysLeft'] <= parameter
                and i['acccountCode'] != 66050
            ]
        return wrapper
    return get_function


def export_to_excel(data):
    filename = 'filename.xlsx'
    dataframe = pd.DataFrame(data)
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        dataframe.to_excel(writer, sheet_name='passwords', index=False)
        worksheet = writer.sheets['passwords']
        for idx, col in enumerate(dataframe.columns):
            column_len = dataframe[col].astype(str).map(len).max()
            column_len = max(column_len, len(col))
            worksheet.set_column(idx, idx, column_len + 2)
    return filename


if __name__ == '__main__':
    PASSWORD_LIFETIME = 90
    str_date = '2025-05-07 14:06:12'
    print(get_pass_lifetime_left(PASSWORD_LIFETIME, str_date))

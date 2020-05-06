from datetime import datetime


def get_format_birthday(iin):
    return datetime.strptime(iin[:6], '%y%m%d').date()

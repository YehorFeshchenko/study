def get_date(dt, tz):
    date = dt + tz
    return datetime.datetime.fromtimestamp(date)


def check_city_found(response_list):
    if response_list['cod'] == '404':
        return False
    return True


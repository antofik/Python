__author__ = 'anton'

def clean_email(raw):
    value = raw.strip()
    if '@' not in value:
        return None
    return raw

def clean_phone(raw):
    numbers = ''.join([x for x in raw if x.isdigit()])
    if len(numbers)==11:
        if numbers.startswith('8'):
            numbers = '7' + numbers[1:]
    elif len(numbers)==10:
        numbers = '7' + numbers
    elif len(numbers)==7:
        numbers = '7495' + numbers
        pass
    else: #unknown format
        return None
    value = '+' + numbers
    return value

from inquirer import errors
from datetime import datetime


def serial_number_validate(answer, current):
    if not (isinstance(current, str) and len(str(current)) >= 10):
        raise errors.ValidationError(
            '',
            reason='"{}" is not a valid serial-number. should be at least 10 characters'.format(current)
        )
    else:
        return True


def date_validate(answer, current):
    try:
        datetime.strptime(current, '%Y-%m-%d')
        return True
    except ValueError:
        raise errors.ValidationError(
            '',
            reason='"{}" incorrect date format, should be <YYYY-MM-DD>'.format(current)
        )


def string_validate(answer, current):
    chars_limit = 1
    if not (isinstance(current, str) and len(str(current)) >= chars_limit):
        raise errors.ValidationError(
            '',
            reason='"{}" is not a valid. should be at least {} characters'.format(current, chars_limit)
        )
    else:
        return True


def int_validate(anwer, current):
    digits_limit = 1
    if len(str(current)) < 1:
        raise errors.ValidationError(
            '',
            reason='"{}" is not valid. should be at least {} digits'.format(current, digits_limit)
        )
    try:
        int(current)
        return True
    except ValueError:
        raise errors.ValidationError(
            '',
            reason='"{}" is not valid. should be digit'.format(current)
        )

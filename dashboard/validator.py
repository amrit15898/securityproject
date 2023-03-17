import re


def text_validate(name):
    reg = "[A-Za-z]{2,25}( [A-Za-z]{2,25})?"
    if re.fullmatch(reg, name):
        return False
    else:
        return True

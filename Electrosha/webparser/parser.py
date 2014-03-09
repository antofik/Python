import re

def get_value(pattern, text):
    m = re.match('.*%s.*' % pattern, text, re.MULTILINE|re.DOTALL)
    if m:
        return m.group(1)
    else:
        return None

def get_values(pattern, text):
    m = re.match('.*%s.*' % pattern, text, re.MULTILINE|re.DOTALL)
    if m:
        return m.groups()[1:]
    else:
        return None

def findall(pattern, text):
    return re.findall('%s' % pattern, text, re.MULTILINE|re.DOTALL)
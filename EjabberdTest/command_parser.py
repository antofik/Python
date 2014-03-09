import traceback

from tests import *

class Parser:

    def __init__(self):
        pass

    def parse_file(self, filename):
        with open(filename) as f:
            text = ' '.join(f.readlines())
            f.close()
        return self.parse_text(text)

    def parse_text(self, text):
        lines = [i.strip() for i in text.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ').split(';')]
        commands = []
        comment = False
        for line in lines:
            if line.startswith('###'):
                comment = not comment
                line = line[3:].strip()
            if comment:
                continue
            #print '>>>', line
            command = self.parse_command(line)
            if command:
                commands.append(command)
                command.number = len(commands)
        return commands

    def parse_command(self, line):
        if not line or line.startswith('#'):
            return None
        try:
            line = re.sub(r'^([a-zA-Z]*?)\(', r'\1Command(', line)
            command = eval(line)
            return command
        except Exception, e:
            raise


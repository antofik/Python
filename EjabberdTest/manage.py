import command_parser
from tests import *
import xmpp.auth
import sys

verbose = False

def print_usage():
    print 'Ejabberd tests usage:\n'
    print '\t\tpython manage.py [debug] [verbose] filename1 filename2 filename3...'

def output_error(title, message):
    print '%s;2;%s' % (title, message)

def output_ok(title, message):
    print '%s;0;%s' % (title, message)

def main():
    global verbose

    if len(sys.argv)<2:
        print_usage()
        return

    files = []
    debug = False
    verbose = False
    for arg in sys.argv[1:]:
        if arg=='debug':
            debug = True
            continue
        if arg=='verbose':
            verbose = True
            continue
        files.append(arg)

    if not debug:
        xmpp.debug.Debug = xmpp.Debug.NoDebug

    if not files:
        print_usage()
        return

    for file in files:
        try:
            p = command_parser.Parser()
            commands = p.parse_file(file)

            script_test = ScriptedTest(commands, file, verbose)
            script_test.execute()
            if script_test.ok:
                output_ok(script_test.title, 'Ok')
            else:
                errors = 'Errors:' '\n'.join(script_test.errors)
                output_error(script_test.title, errors)
        except Exception, e:
            output_error(file, e.message or str(e))


if __name__=='__main__':
    main()
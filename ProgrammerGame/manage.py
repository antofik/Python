import sys
from clint.textui import colored
from Server import Server

def main():
    print colored.blue("Programmer's Game Management Console version 0.1")
    parse_args()

def parse_args():
    if 'server' in sys.argv:
        start_server()
    elif 'cliennt' in sys.argv:
        start_client()
    else:
        start_server()

def start_client():
    pass

def start_server():
    Server.create()

if __name__=='__main__':
    main()
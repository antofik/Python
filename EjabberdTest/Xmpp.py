# coding=utf-8
import random
import traceback
from xmpp import *

class Xmpp:
    def __init__(self, server, login = None, password = ''):
        self.client = Client('xmpp.redhelper.ru')
        self.login = login
        self.password = password
        self.server = server
        self.incoming = {}
        self.outcoming = {}
        self.last_received = None
        self.id = 0
        self.iqs = {}
        self.last_iq = None
        self.params = {'login':login, 'password':password, 'server':server}

    def connect(self):
        try:
            if not self.client.connect(server=self.server):
                return False, "Can not connect to server %s" % str(self.server)
            ok, error = self.auth(self.login, self.password)
            if not ok:
                return False, error
            self.register_handlers()
            self.client.sendInitPresence(requestRoster=0)
            self.process()
            return True, None
        except Exception, e:
            traceback.print_exc()
            return False, str(e)

    def auth(self, login, password):
        if not self.client.auth(login, password, "RedHelper" if login else "t_visitor"):
            return False, "Can not auth with server: login=%s, password=%s" % (login, password)
        return True, None

    def send_iq(self, type, ns, payload = '', timeout = 10, to = None):
        delay = 0.1
        try:
            iq = Iq(typ=type, queryNS=ns, payload=payload)
            if to:
                iq.setTo(to)
            id = random.randint(900000000, 999999999)
            iq.setID(id)
            self.iqs[id] = None
            self.client.send(iq)
            spent = 0
            while not self.iqs[id] and spent<timeout:
                self.client.Process(delay)
                spent += delay
            iq = self.iqs[id]
            del self.iqs[id]
            return iq
        except Exception,e:
            import traceback
            traceback.print_exc()
            print 'error <%s>' % str(e)
            return None

    def register_handlers(self):
        self.client.RegisterHandler('presence', self.on_presence)
        self.client.RegisterHandler('iq', self.on_iq)
        self.client.RegisterHandler('message', self.on_message)
        self.client.RegisterHandler('error', self.on_error)
        self.client.RegisterHandler('stream:error', self.on_error)

    def on_error(self, connection, stanza):
        print '-----------------------------------> Error received!' + str(stanza)
        pass

    def on_presence(self, connection, presence):
        pass

    def on_iq(self, connection, iq):
        self.iqs[int(iq.getID())] = iq

    def on_message(self, connection, message):
        self.last_received = message
        self.incoming[message.getID()] = message

    def send_message(self, message, attributes):
        self.id += 1
        for attributeName in attributes:
            message.setAttr(attributeName, attributes[attributeName])
        self.outcoming[self.id] = message
        self.client.send(message)

    def disconnect(self):
        pass

    def process(self, time = 1):
        self.client.Process(time)
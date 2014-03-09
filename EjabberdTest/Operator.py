# coding=utf-8
import uuid
from xmpp import *
from Xmpp import Xmpp

class Operator(Xmpp):
    def __init__(self, server, login, password):
        Xmpp.__init__(self, server, login, password)

    def getJID(self):
        return '%s@operator.xmpp.redhelper.ru' % self.login

    def getShortJID(self):
        return '%s@xmpp.redhelper.ru' % self.login

    def send_test_message(self, to):
        return self.send_message(to, 'Test message: %s' % str(uuid.uuid1()))

    def send_message(self, to, text, attributes):
        message = Message(to=to, frm='%s@xmpp.redhelper.ru' % self.login, body = text)
        Xmpp.send_message(self, message, attributes)
        return message.getID()

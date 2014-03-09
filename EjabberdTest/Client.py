# coding=utf-8
import uuid
import random
from xmpp import *
from Xmpp import Xmpp

class Client(Xmpp):
    def __init__(self, server):
        Xmpp.__init__(self, server)
        self.vid = random.randint(9000000, 9999999)
        self.params['vid'] = self.vid

    def getJID(self):
        return '%s@visitor.xmpp.redhelper.ru' % self.vid

    def getShortJID(self):
        return '%s@xmpp.redhelper.ru' % self.vid

    def send_test_message(self, to):
        return self.send_message(to, 'Test message: %s' % str(uuid.uuid1()))

    def send_message(self, to, text, attributes):
        message = Message(to=to, body = text)
        message.setAttr('jid', self.getShortJID())
        Xmpp.send_message(self, message, attributes)
        return message.getID()


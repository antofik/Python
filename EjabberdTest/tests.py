# coding=utf-8
import re
from threading import  Thread, Event
import time
from Client import Client
from Operator import Operator

class GeneralTest:
    def __init__(self, title):
        self.title = title
        self.ok = False
        self.errors = []

    def execute(self):
        print 'Test "%s" not implemented' % self.title

class ScriptedTest(GeneralTest):
    def __init__(self, commands, title, debug):
        GeneralTest.__init__(self, title)
        self.xmpps = {}
        self.current_command = None
        self.threads = []
        self.last_iq = None
        self.commands = commands
        self.debug = debug
        self.error_message = 'Error'

    def execute(self):
        global debug
        self.stop = False
        for command in self.commands:
            if self.debug:
                print 'Executing command [%s] %s %s' % (command.number, command.__class__.__name__, command.id)
            self.execute_command(command)
            command.wait()
            if self.errors:
                break
        self.ok = not self.errors

    def execute_command(self, command):
        self.current_command = command
        if isinstance(command, CreateContextCommand):
            th = Thread(target=self.thread, args = (command,))
            th.daemon = True
            self.threads.append(th)
            self.current_command = None
            th.start()
        elif isinstance(command, ExecuteInContextCommand):
            pass
        elif isinstance(command, SetErrorMessageCommand):
            command.process(self)
            command.complete()
            self.current_command = None
        else:
            raise Exception("Unknown command type")

    def thread(self, create_command):
        command = None
        try:
            id = create_command.id
            ok, xmpp = create_command.process()
            if not ok:
                raise Exception(xmpp)
            if xmpp.client.isConnected:
                self.xmpps[id] = xmpp
                create_command.complete()
            else:
                raise Exception("Cannot connect: %s" % id)
            while not self.stop:
                command = self.current_command
                if command is not None and command.id == id:
                    self.current_command = None
                    ok, error = command.process(self)
                    if not ok:
                        raise Exception(error)
                    command.complete()
                elif command:
                    command.wait()
                else:
                    xmpp.client.Process(0.1)
        except Exception, e:
            self.errors.append('%s [%s]' % (self.error_message, e.message))
            self.ok = False
            self.stop = True
            create_command.complete()
            if command:
                command.complete()


class BaseCommand:
    def __init__(self):
        self.id = None
        self.done = Event()

    def wait(self):
        self.done.wait()

    def complete(self):
        self.done.set()


class CreateContextCommand(BaseCommand):
    def __init__(self):
        BaseCommand.__init__(self)

    def process(self):
        return None


class ExecuteInContextCommand(BaseCommand):
    def __init__(self):
        BaseCommand.__init__(self)

    def process(self, context):
        pass


class CreateOperatorCommand(CreateContextCommand):
    def __init__(self, id, server, login, password):
        CreateContextCommand.__init__(self)
        self.server = server
        self.login = login
        self.password = password
        self.id = id

    def process(self):
        self.operator = Operator(self.server, self.login, self.password)
        ok, error = self.operator.connect()
        return ok, self.operator if ok else error


class CreateVisitorCommand(CreateContextCommand):
    def __init__(self, id, server, previous_operator = None, required_operator = None):
        CreateContextCommand.__init__(self)
        self.id = id
        self.server = server
        self.previous_operator = previous_operator
        self.required_operator = required_operator

    def process(self):
        self.visitor = Client(self.server)
        ok, error = self.visitor.connect()
        return ok, self.visitor if ok else error


class SendIqCommand(ExecuteInContextCommand):
    def __init__(self, id, type, xmlns, payload = "", to=None):
        ExecuteInContextCommand.__init__(self)
        self.id = id
        self.type = type
        self.xmlns = xmlns
        self.payload = payload
        self.to = to

    def process(self, context):
        try:
            xmpp = context.xmpps[self.id]
            payload = self.payload.format(**xmpp.params)
            if self.to:
                target = context.xmpps[self.to]
                self.to = target.getShortJID()
            iq = xmpp.send_iq(self.type, self.xmlns, payload, to=self.to)
            xmpp.last_iq = iq
            if iq is None:
                return False, 'Server did not respond on IQ type=%s, xmlns=%s, payload=%s' % (self.type, self.xmlns, payload)
            if iq.getType()!='result':
                return False, 'Server did not respond with result on IQ type=%s, xmlns=%s, payload=%s. Result = %s' % (self.type, self.xmlns, payload, iq)
            return True, iq
        except Exception, e:
            return False, e.message or str(e)


class SetErrorMessageCommand(BaseCommand):
    def __init__(self, message):
        BaseCommand.__init__(self)
        self.message = message

    def process(self, context):
        context.error_message = self.message


class VerifyResultIqCommand(ExecuteInContextCommand):
    def __init__(self, id, regex):
        ExecuteInContextCommand.__init__(self)
        self.id = id
        self.regex = regex

    def process(self, context):
        try:
            xmpp = context.xmpps[self.id]
            if not xmpp.last_iq:
                return False, 'No iq results to verify'
            m = re.search(self.regex.format(**xmpp.params), unicode(xmpp.last_iq))
            if m:
                return True, None
            else:
                return False, 'Verification on %s failed' % self.regex
        except Exception, e:
            return False, e.message or str(e)


class GetMessageAttributeCommand(ExecuteInContextCommand):
    def __init__(self, id, attribute):
        ExecuteInContextCommand.__init__(self)
        self.id = id
        self.attribute = attribute

    def process(self, context):
        try:
            xmpp = context.xmpps[self.id]
            message = xmpp.last_received
            if not message:
                return False, 'No message to extract attribute from'
            attribute = message.getAttr(self.attribute)
            if not attribute:
                return False, "Attribute %s not found in message %s" % (self.attribute, unicode(message))
            xmpp.params[self.attribute] = attribute
            return True, None
        except Exception, e:
            return False, e.message or str(e)


class SendMessageCommand(ExecuteInContextCommand):
    def __init__(self, id, toid, message, attributes = None):
        ExecuteInContextCommand.__init__(self)
        self.id = id
        self.toid = toid
        self.message = message
        self.attributes = attributes or {}

    def process(self, context):
        try:
            xmpp = context.xmpps[self.id]
            target = context.xmpps[self.toid]
            to = target.getJID()
            for attributeName in self.attributes:
                self.attributes[attributeName] = self.attributes[attributeName].format(**xmpp.params)
            id = xmpp.send_message(to, self.message, self.attributes)
            xmpp.process()
            return True, id
        except Exception,e:
            return False, e.message or str(e)


class ReceiveMessageCommand(ExecuteInContextCommand):
    def __init__(self, id, fromid, message, timeout = 10):
        ExecuteInContextCommand.__init__(self)
        self.id = id
        self.fromid = fromid
        self.message = message
        self.interval = 0.1
        self.timeout = timeout

    def process(self, context):
        try:
            xmpp = context.xmpps[self.id]
            waiting = 0
            ok = False
            while waiting<self.timeout:
                xmpp.process(self.interval)
                for id in xmpp.incoming:
                    message = xmpp.incoming[id]
                    if message.getBody()==self.message:
                        ok = True
                        break
                if ok:
                    break
                waiting += self.interval
            if not ok:
                return False, "%s did not received required message <%s> in %s seconds. Last received message: %s" % (self.id, self.message, self.timeout, xmpp.last_received)
            return True, None
        except Exception, e:
            return False, e.message or str(e)





import json
import random
import socket
import struct
from threading import Thread
import time
import traceback
import uuid
import signal
import atexit

class Server:
    clients = []

    @staticmethod
    def create(port = 5007, host = None):
        """Factory method for starting new instance of server"""
        Server.instance = Server(port, host)
        Server.thread = Thread(target=Server.instance.start)
        Server.thread.start()
        atexit.register(Server.close)
        signal.signal(signal.SIGTERM, lambda signum, stack_frame: Server.close)
        signal.signal(signal.SIGBREAK, lambda signum, stack_frame: Server.close)
        raw_input()
        Server.instance.socket.close()
        del Server.instance.socket
        print 'Shutting down'

    def __init__(self, port, host):
        self.port = port
        self.host = host

    def start(self):
        self.socket = socket.socket()
        host = self.host or socket.gethostname()
        print 'Host=%s' % host
        print 'binding...'
        self.socket.bind((host, self.port))
        print 'listening'
        self.socket.listen(5)
        while True:
            remote_socket, address = self.socket.accept()
            print 'New player connected: ', address
            connector = Player(remote_socket, address)
            connector.run()

    @staticmethod
    def close():
        print 'Closing...'

class Player:
    NONE = 0
    CREATED = 1
    JOINED = 2

    Games = {}

    def __init__(self, socket, address):
        self.socket = socket
        self.address = address
        self.state = Player.NONE
        self.id = str(uuid.uuid1())
        self.offsetX, self.offsetY = 0,0

    def run(self):
        self.thread = Thread(target=self.process)
        self.thread.start()

    def process(self):
        while True:
            header = b''
            while len(header)<16:
                try:
                    header += self.socket.recv(16 - len(header))
                except Exception:
                    print 'Disconnected'
                    break
            try:
                signature, version, length = struct.unpack('=2sHQ4x', header)
                if length<1 or length>10240:
                    raise Exception('Invalid packet: bad size %s' % length)
                data = b''
                while len(data)<length:
                    data += self.socket.recv(length - len(data))
                print 'Data received:', data
                self.parse(data)
            except Exception, e:
                print 'Error while parsing data'
                traceback.print_exc()
                break

    def parse(self, data):
        print 'Command received'
        data = json.loads(data)
        if 'command' not in data:
            raise Exception('Invalid packet: no command present')
        command = data['command']
        id = data['id']
        response = {'id':id, 'type':'response', 'command': command}
        if command=='create':
            print '[create]'
            if self.state != Player.NONE:
                raise Exception("Invalid operation")
            nodes = data['nodes']
            try:
                self.game = Game()
                response['game'] = self.game.id
                Player.Games[self.game.id] = self.game
                self.game.add_player(nodes, self)
                response['ok'] = True
                self.state = Player.CREATED
            except GameError, e:
                response['ok'] = False
                response['error'] = str(e)
        elif command=='join':
            print '[join]'
            if self.state != Player.NONE:
                raise Exception("Invalid operation")
            gameid = data['game']
            nodes = data['nodes']
            if gameid in Player.Games:
                self.game = Player.Games[gameid]
                self.game.add_player(nodes, self)
                response['ok'] = True
                self.state = Player.JOINED
            else:
                response['ok'] = False
                response['error'] = 'Game not found'
        elif command=='move':
            print '[move]'
            if self.state == Player.NONE:
                raise Exception("Invalid operation")
            from_node = data['from']
            to_node = data['to']
            response['ok'], response['error'] = self.game.move(from_node, to_node, self)
        elif command=='see':
            print '[see]'
            if self.state == Player.NONE:
                raise Exception("Invalid operation")
            eye = data['eye']
            direction = data['direction']
            response['ok'], response['type'] = self.game.see(eye, direction, self)
        else:
            print '[unknown]'
            raise Exception("Unknown command")
        self.send(response)
        self.game.cycle()

    def send(self, response):
        data = json.dumps(response)
        header = struct.pack('=2sHQ4x', 'AI', 1, len(data))
        packet = header + data
        self.socket.sendall(packet)

    def send_killed(self, killed):
        response = {'id':str(uuid.uuid1()),'command':'destroyed', 'type':'notification', 'cells': killed}
        self.send(response)

class Game:
    HEIGHT = 400
    WIDTH = 400

    def __init__(self):
        self.id = str(uuid.uuid1())
        self.create_map()
        self.players = {}

    def add_player(self, json_nodes, player):
        """ add new player to the game """
        self.players[player.id] = player
        player.offsetX = random.randint(100, Game.WIDTH - 100)
        player.offsetY = random.randint(100, Game.HEIGHT - 100)

        i = 0
        for json in json_nodes:
            node = Node(json, player.id, i)
            x = node.x + player.offsetX
            y = node.y + player.offsetY
            if (x,y) in self.map:
                self.map[(x, y)].nodes.append(node)
                i += 1

    def create_map(self):
        self.map = {}
        for x in xrange(Game.WIDTH):
            for y in xrange(Game.HEIGHT):
                self.map[(x,y)] = MapNode()
        for x in xrange(Game.WIDTH):
            for y in xrange(Game.HEIGHT):
                for dx in [-1,0,1]:
                    for dy in [-1,0,1]:
                        if (x+dx, y+dy) in self.map and not (dx==0 and dy==0):
                            self.map[(x,y)].neighbours.append(self.map[(x+dx, y+dy)])

    def cycle(self):
        self.condemn()
        self.remove_killed()

    def rule_condemn(self, mapnode, node):
        ok, ttl = (False, 0)
        n = mapnode.count(node.playerid)
        if n>=2:
            ok = True
        print 'checking node', node.id,'(', id(node), '):', n
        return ok, ttl

    def condemn(self):
        """ Search for nodes, which cannot live anymore and condemns them to death """
        for position in self.map:
            mapnode = self.map[position]
            for node in mapnode.nodes:
                if node.state==Node.ALIVE:
                    ok, ttl = self.rule_condemn(mapnode, node)
                    if not ok:
                        node.state = Node.CONDEMNED
                        node.ttl = ttl
                elif node.state==Node.CONDEMNED:
                    node.ttl -= 1
                    if node.ttl<=0:
                        node.state = Node.KILLED

    def remove_killed(self):
        killed = {}
        for position in self.map:
            mapnode = self.map[position]
            for node in list(mapnode.nodes):
                if node.state==Node.KILLED:
                    mapnode.nodes.remove(node)
                    if node.playerid not in killed:
                        killed[node.playerid] = []
                    killed[node.playerid].append(node.id)
        if killed:
            print 'Found killed cells. Removing them...'
            for playerid in killed:
                nodes = killed[playerid]
                self.players[playerid].send_killed(nodes)

    def move(self, from_node, to_node, player):
        fx,fy = int(from_node[0]) + player.offsetX, int(from_node[1]) + player.offsetY
        tx,ty = int(to_node[0]) + player.offsetX, int(to_node[1]) + player.offsetY
        if (fx,fy) not in self.map or (tx, ty) not in self.map:
            return False, 'source cell does not belong to player'
        source = self.map[(fx, fy)]
        target = self.map[(tx, ty)]
        for node in list(source.nodes):
            if node.playerid==player.id:
                if node.state!=Node.ALIVE:
                    return False, 'cell is not alive'
                if target.count(player.id, node.id)<2:
                    return False, 'target position contains less then 2 other cells'
                for cell in target.nodes:
                    if cell.playerid==player.id:
                        return False, 'target position already contains your cell'
                    else:
                        self.kill_cell(cell)
                source.nodes.remove(node)
                target.nodes.append(node)
        return True, 'ok'

    def kill_cell(self, cell):
        self.players[cell.playerid].send_killed([cell.id])

    def see(self, eye, direction, player):
        fx,fy = eye[0] + player.offsetX, eye[1] + player.offsetY
        tx,ty = fx + direction[0], fy + direction[1]
        if abs(direction[0]) + abs(direction[1]) > 3:
            return False, -1
        if (fx,fy) not in self.map or (tx, ty) not in self.map:
            return False, -1
        source = self.map[(fx, fy)]
        target = self.map[(tx, ty)]
        for node in list(source.nodes):
            if node.playerid==player.id:
                if node.state!=Node.ALIVE:
                    return False, -1
                if target.count(player.id)<2:
                    return False
                for i in target.nodes:
                    if i.playerid!=player.id:
                        return True, i.type
                return True, -1
        return False, -1

class MapNode:
    def __init__(self):
        self.nodes = []
        self.neighbours = []

    def count(self, playerid, exceptid = None):
        n = 0
        for mapnode in self.neighbours:
            for node in mapnode.nodes:
                if node.playerid==playerid:
                    if node.id != exceptid:
                        n += 1
        print 'node %s has %s neighbours' % (id(self), n)
        return n

class Node:
    ALIVE = 0
    CONDEMNED = 1
    KILLED = 2
    REMOVED = 3

    def __init__(self, json, playerid, id):
        if len(json)<3:
            raise Exception('Node description contains invalid number of values')
        self.x = int(json[0])
        self.y = int(json[1])
        self.type = int(json[2])
        self.state = Node.ALIVE
        self.ttl = 0
        self.id = id
        self.playerid = playerid

class GameError:
    def __init__(self, message):
        self.message = message

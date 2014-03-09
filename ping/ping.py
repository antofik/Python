import sys
import socket
import array
import struct
import time
import select
import binascii
import signal

ICMP_TYPE = 8
ICMP_CODE = 0
ICMP_CHECKSUM = 0
ICMP_ID = 0
ICMP_SEQ_NR = 0

payload = b'\x00'
Size = 100

def signal_handler(signal, frame):
    print('Ctrl+C pressed, breaking program')
    sys.exit(0)

def Initialize():
    #signal.signal(signal.SIGINT, signal_handler)
    pass
   
def CreateICMPpacket(id, size = 0):
    header = struct.pack('bbHHh', ICMP_TYPE, ICMP_CODE, ICMP_CHECKSUM, ICMP_ID, ICMP_SEQ_NR + id)
    data = struct.pack('d', time.time())
    packet = header + data
 
    payload = b'\x00'
    if size>len(packet):
        payload = b'X' * (size - len(packet))
        packet += payload
    checksum = CalculateChecksum(packet)
    header = struct.pack('bbHHh', ICMP_TYPE, ICMP_CODE, checksum, ICMP_ID, ICMP_SEQ_NR + id)
    packet = header + data + payload
    return packet
    
def CreateSocket(node = None, size = 0):
    host = socket.gethostbyname(node)
    print('\nPinging %s [%s] with %d bytes of data:' % (node, host, size))
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    return {'s':s, 'host':host}
    

def sendPacket(id, s, host, size = 0, timeout = 1.0):
    try:
        packet = CreateICMPpacket(id, size)
        s.sendto(packet, (host,1))
        waited = 0
        while 1:
            input, output, exception = select.select([s], [], [], 0.1)
            waited += 0.1
            if input:
                break
            if waited>timeout:
                break
        if input:
            endtime = time.time()
            ipPacket, address = s.recvfrom(len(packet) + 128)        
            #print(binascii.hexlify(ipPacket))
            ttl = ipPacket[8]
            icmpPacket = ipPacket[20:28]
            icmpType, icmpCode, icmpChksum, icmpID, icmpSeqnr = struct.unpack("bbHHh", icmpPacket)
            starttime = struct.unpack('d', ipPacket[28:36])[0]
            delta = 1000*(endtime - starttime)
            print('Reply from %s: bytes=%d time=%dms TTL=%s' % (host, size, delta, ttl))
        else:
            print('Request timed out.')
    except(EOFError, KeyboardInterrupt):
        print('Keyboard interrupt')
        sys.exit(0)

def CalculateChecksum(data):
    sum = 0
    
    if len(data)&1:
        data = data + '\0'

    words = array.array('h', data)
    
    for word in words:
        sum += (word & 0xffff)

    sum = (sum>>16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    return (~sum) & 0xffff
    
Initialize()
sock = CreateSocket('mfst.pro', Size)
for seq in range(4):
    sendPacket(seq, sock['s'], sock['host'], Size, 4)

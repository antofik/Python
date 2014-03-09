#include <winsock.h>

#define HOST_NAME "www.sources.ru" // ����� �������� ���
#define WINSOCK_VERSION 0x0101 // ������ ������� 1.1
#define NO_FLAGS 0 // ����� �� ���������
// � RFC 792 ���������� �������� ��������� ICMP
#define ICMP_ECHO 8 // An ICMP echo message
#define ICMP_ECHOREPLY 0 // An ICMP echo reply message
#define ICMP_HEADERSIZE 8 

struct ip // ��������� ��������� IP
{
 BYTE ip_verlen; // Version and header length
 BYTE ip_tos; // Type of service
 WORD ip_len; // Total packet length 
 UINT ip_id; // Datagram identification 
 WORD ip_fragoff; // Fragment offset 
 BYTE ip_ttl; // Time to live 
 BYTE ip_proto; // Protocol
 UINT ip_chksum; // Checksum 
 IN_ADDR ip_src_addr; // Source address 
 IN_ADDR ip_dst_addr; // Destination address 
 BYTE ip_data[1]; // Variable length data area
};

struct icmp // ��������� ��������� ICMP
{
 BYTE icmp_type; // Type of message
 BYTE icmp_code; // Type "sub code" (zero for echos)
 WORD icmp_cksum; // 1's complement checksum
 HINSTANCE icmp_id; // Unique ID (the instance handle)
 WORD icmp_seq; // Tracks multiple pings
 BYTE icmp_data[1]; // The start of optional data
};

char szPingBuffer[100];


HINSTANCE hInstance;


WORD InternetChksum(LPWORD lpwIcmpData, WORD wDataLength)
{
 long lSum; // Store the summation
 WORD wOddByte; // Left over byte from the summation
 WORD wAnswer; // The 1's complement checksum

 lSum = 0L;

 while (wDataLength > 1)
 {
 lSum += *lpwIcmpData++;
 wDataLength -= 2;
 }

 // Handle the odd byte if necessary and make sure the top half is zero
 if (wDataLength == 1)
 {
 wOddByte = 0;
 *((LPBYTE) &wOddByte) = *(LPBYTE)lpwIcmpData; // One byte only
 lSum += wOddByte;
 }

 // Add back the carry outs from the 16 bits to the low 16 bits
 lSum = (lSum >> 16) + (lSum & 0xffff); // Add high-16 to low-16
 lSum += (lSum >> 16); // Add carry
 wAnswer = (WORD)~lSum; // 1's complement, then truncate 
 // to 16 bits
 return(wAnswer);
}


BOOL DoPingOperation(HANDLE hInstance)
{
 // ��������� ����������
int iPacketSize; // ������ ICMP-������ 
int iHostAddrLength; // ����� ������ �������� ����������
int iIPHeadLength; // ����� ��������� IP-����������
int iReceivedBytes; // ���������� �������� ������
int iSentBytes; // ���������� ��������� ������
int nProtocol; // ����� ��������� ICMP
int iSocketError; // �������� ���� ������
PDWORD pdwTimeStamp; // ������� "�����" ��� ��������
DWORD dwReturnTime; // ������� "�����" ��� ������
DWORD dwRoundTrip; // ������� "�����" �������� ������� �������
 // ���������, ��������� � WINSOCK.H
SOCKADDR_IN sockAddrLocal; // ��������� ������ ������
SOCKADDR_IN sockAddrHost; // 
SOCKET hSocket; // ���������� ������
LPHOSTENT lpHostEntry; // ��������� ������ �
 // ����������� � ������� ����������
LPPROTOENT lpProtocolEntry; // ��������� ������ � ����������� � ���������

BYTE IcmpSendPacket[1024]; // ����� ��� ���������� ������
BYTE IcmpRecvPacket[4096]; // ����� ��� ����������� ������ 

struct icmp *pIcmpHeader; // ��������� �� ��������� ICMP
struct ip *pIpHeader; // ��������� �� ���������-��������� IP
LPSTR lpszHostName; // ��������� �� ��������� ������ �������

lpszHostName = HOST_NAME;

if ((lpHostEntry = gethostbyname(HOST_NAME)) == NULL) {
 wsprintf(szPingBuffer, "Could not get %s IP address.", (LPSTR)lpszHostName);
 return(FALSE);
}

sockAddrLocal.sin_family = AF_INET;
sockAddrLocal.sin_addr = *((LPIN_ADDR) *lpHostEntry->h_addr_list);

// � ������ �������� ������, �� ������ ��������� ��������
if ((lpProtocolEntry = getprotobyname("icmp")) == NULL)
 nProtocol = IPPROTO_ICMP;
else
 nProtocol = lpProtocolEntry->p_proto;

// ������� ������� ����� � ��������� ICMP � �������� ���������
if ((hSocket = socket(PF_INET, SOCK_RAW, nProtocol)) == INVALID_SOCKET)
{
 wsprintf(szPingBuffer, "Could not create a RAW socket.");
 return(FALSE);
}

pIcmpHeader = (struct icmp *) IcmpSendPacket; // Point at the data area
pIcmpHeader->icmp_type = ICMP_ECHO; // then fill in the data.
pIcmpHeader->icmp_code = 0; // Use the Sockman instance 
pIcmpHeader->icmp_id = hInstance; // handle as a unique ID.
pIcmpHeader->icmp_seq = 0; // It's important to reset
pIcmpHeader->icmp_cksum = 0; // the checksum to zero.

//�������� �������� "�����" ������������� � �������������� ������� ������
pdwTimeStamp = (PDWORD)&IcmpSendPacket[ICMP_HEADERSIZE];
*pdwTimeStamp = GetTickCount();
iPacketSize = ICMP_HEADERSIZE + sizeof(DWORD);
pIcmpHeader->icmp_cksum = InternetChksum((LPWORD)pIcmpHeader, iPacketSize);

if (pIcmpHeader->icmp_cksum !=0 )
{ 
 iSentBytes = sendto(hSocket, (LPSTR) IcmpSendPacket, iPacketSize, 
 NO_FLAGS, (LPSOCKADDR) &sockAddrLocal, sizeof(sockAddrLocal));
 if (iSentBytes == SOCKET_ERROR) {
 closesocket(hSocket);
 wsprintf(szPingBuffer,
 "The sendto() function returned a socket error.");
 return(FALSE);
 }

 if (iSentBytes != iPacketSize) {
 closesocket(hSocket);
 wsprintf(szPingBuffer,
 "Wrong number of bytes sent: %d", iSentBytes);
 return(FALSE);
 }

 iHostAddrLength = sizeof(sockAddrHost);

 iReceivedBytes = recvfrom(hSocket, (LPSTR) IcmpRecvPacket, 
 sizeof(IcmpRecvPacket), NO_FLAGS, (LPSOCKADDR) &sockAddrHost,
 &iHostAddrLength);
}
else {
 closesocket(hSocket);
 wsprintf(szPingBuffer, "Checksum computation error! Result was zero!");
 return(FALSE);
}

closesocket(hSocket);

if (iReceivedBytes == SOCKET_ERROR) { 
 iSocketError = WSAGetLastError();
 if (iSocketError == 10004) {
 wsprintf(szPingBuffer,
 "Ping operation for %s was cancelled.", 
 (LPSTR)lpszHostName);
 dwRoundTrip = 0;
 return(TRUE);
 }
 else {
 wsprintf(szPingBuffer,
 "Socket Error from recvfrom(): %d", iSocketError);
 return(FALSE);
 }
}

dwReturnTime = GetTickCount();
dwRoundTrip = dwReturnTime - *pdwTimeStamp;

// ��������� �� IP-��������� ��������� ������
pIpHeader = (struct ip *)IcmpRecvPacket;

// ��������� ���� 4-7 � ����������� ���������� �2-������ ���� � ���������� ������
iIPHeadLength = (pIpHeader->ip_verlen >> 4) << 2;

// ��������� �����, ����� ��������������, ��� ICMP-��������� ������
if (iReceivedBytes < iIPHeadLength + ICMP_HEADERSIZE) {
 wsprintf(szPingBuffer, "Received packet was too short.");
 return(FALSE);
}

// ��������� �� ICMP-���������, ��������� ����� �� IP-����������
pIcmpHeader = (struct icmp *) (IcmpRecvPacket + iIPHeadLength);

// ���������, ��� �� ������� ������ "���"-�����
if (pIcmpHeader->icmp_type != ICMP_ECHOREPLY) {
 wsprintf(szPingBuffer,
 "Received packet was not an echo reply to your ping.");
 return(FALSE);
}

// ���������, ����������� �� ���� ����� ����� ���������
if (pIcmpHeader->icmp_id != (HINSTANCE)hInstance) {
 wsprintf(szPingBuffer,
 "Received packet was not sent by this program.");
 return(FALSE);
}

// ��, ���� ����� ��� ������ ����� ����������. ��������
// �������� �� IP-����� � ��� ���������� ����������,
// ���������� "���"-�����
lstrcpy(lpszHostName, (LPSTR)lpHostEntry->h_name);
wsprintf(szPingBuffer,
 "Round-trip travel time to %s [%s] was %d milliseconds.",
 (LPSTR)lpszHostName, (LPSTR)inet_ntoa(sockAddrHost.sin_addr), 
 dwRoundTrip);

return(TRUE); 
}


void main ()
{
 WSADATA wsaData;

 WSAStartup(WINSOCK_VERSION, &wsaData);

 DoPingOperation(hInstance);
 MessageBox(NULL, szPingBuffer, "www.sources.ru", MB_OK|MB_ICONSTOP);

 WSACleanup();
}  
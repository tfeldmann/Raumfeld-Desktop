import socket
import mimetools
from StringIO import StringIO


def discover(service, timeout=2, retries=1):
    group = ("239.255.255.250", 1900)
    message = "\r\n".join([
        'M-SEARCH * HTTP/1.1',
        'HOST: {0}:{1}'.format(*group),
        'MAN: "ssdp:discover"',
        'ST: {st}', 'MX: 1', '', ''])
    socket.setdefaulttimeout(timeout)
    responses = {}
    for _ in range(retries):
        sock = socket.socket(socket.AF_INET,
                             socket.SOCK_DGRAM,
                             socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        sock.sendto(message.format(st=service), group)
        while True:
            try:
                response, addr = sock.recvfrom(1024)
                responses[addr[0]] = response
                print mimetools.Message(StringIO(response)).headers
                print response
            except socket.timeout:
                break
    return responses

devices = discover('ssdp:urn:schemas-upnp-org:device:MediaRenderer:1')
for device in devices:
    print "test",

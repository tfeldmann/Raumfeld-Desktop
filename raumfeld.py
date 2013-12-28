import socket
from pysimplesoap.client import SoapClient


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
                print response
            except socket.timeout:
                break
    return responses


# devices = discover('ssdp:urn:schemas-upnp-org:device:MediaRenderer:1')
# for device in devices:
#     print device

rendering_control = SoapClient(
    location="http://192.168.178.37:42342/RenderingService/Control",
    action="urn:upnp-org:serviceId:RenderingControl#",
    namespace="http://schemas.xmlsoap.org/soap/envelope/",
    soap_ns='soap', ns='s', exceptions=True)

av_transport = SoapClient(
    location="http://192.168.178.37:42342/TransportService/Control",
    action="urn:schemas-upnp-org:service:AVTransport:1#",
    namespace="http://schemas.xmlsoap.org/soap/envelope/",
    soap_ns='soap', ns='s', exceptions=True)

# response = av_transport.Play(InstanceID=1, Speed=2)
response = av_transport.Pause(InstanceID=1)
# response = av_transport.Play(InstanceID=1)
# response = rendering_control.SetVolume(InstanceID=1, DesiredVolume=0)
# response = rendering_control.SetMute(InstanceID=1, DesiredMute=0)

# response = rendering_control.GetVolume(InstanceID=1)
# print response.CurrentVolume

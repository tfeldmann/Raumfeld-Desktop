import socket
from pysimplesoap.client import SoapClient


def discover(service='ssdp:all', timeout=2, retries=1):
    group = ("239.255.255.250", 1900)
    message = "\r\n".join([
        'M-SEARCH * HTTP/1.1',
        'HOST: {0}:{1}'.format(*group),
        'MAN: "ssdp:discover"',
        'ST: {st}', 'MX: 1', '', ''])
    socket.setdefaulttimeout(timeout)
    responses = {}
    for _ in range(retries):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
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


class RaumfeldDevice(object):

    def __init__(self, ip, port):
        self.address = 'http://%s:%s' % (ip, port)
        self.rendering_control = SoapClient(
            location='%s/RenderingService/Control' % self.address,
            action='urn:upnp-org:serviceId:RenderingControl#',
            namespace='http://schemas.xmlsoap.org/soap/envelope/',
            soap_ns='soap', ns='s', exceptions=True)

        self.av_transport = SoapClient(
            location='%s/TransportService/Control' % self.address,
            action='urn:schemas-upnp-org:service:AVTransport:1#',
            namespace='http://schemas.xmlsoap.org/soap/envelope/',
            soap_ns='soap', ns='s', exceptions=True)

    def play(self):
        self.av_transport.Play(InstanceID=1, Speed=2)

    def pause(self):
        self.av_transport.Pause(InstanceID=1)

    def set_volume(self, volume):
        self.rendering_control.SetVolume(InstanceID=1, DesiredVolume=volume)

    def get_volume(self):
        response = self.rendering_control.GetVolume(InstanceID=1)
        return response.CurrentVolume

    def set_mute(self, mute):
        self.rendering_control.SetMute(InstanceID=1, DesiredMute=mute)


if __name__ == '__main__':
    devices = discover('ssdp:urn:schemas-upnp-org:device:MediaRenderer:1')
    print devices
    box = RaumfeldDevice(ip='192.168.178.37', port=42342)
    box.pause()

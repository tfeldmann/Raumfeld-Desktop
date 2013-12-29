import socket
import urlparse
from pysimplesoap.client import SoapClient
from pysimplesoap.simplexml import SimpleXMLElement
from pysimplesoap.helpers import fetch
from pysimplesoap.transport import get_Http


def discover(raumfeld_devices_only=True, timeout=2, retries=1):
    """
    Discovers Raumfeld devices in the network
    """
    locations = []
    group = '239.255.255.250', 1900
    message = '\r\n'.join(['M-SEARCH * HTTP/1.1',
                           'HOST: {0}:{1}'.format(*group),
                           'MAN: "ssdp:discover"',
                           'ST: {st}',
                           'MX: 1', '', ''])

    if raumfeld_devices_only:
        service = 'ssdp:urn:schemas-upnp-org:device:MediaRenderer:1'
    else:
        service = 'ssdp:all'

    socket.setdefaulttimeout(timeout)
    for _ in range(retries):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                             socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        sock.sendto(message.format(st=service), group)
        while True:
            try:
                response = sock.recv(2048)
                for line in response.split('\r\n'):
                    if line.startswith('Location: '):
                        location = line.split(' ')[1].strip()
                        if not location in locations:
                            locations.append(location)
            except socket.timeout:
                break
    devices = [RaumfeldDevice(location) for location in locations]

    # only return 'Digital Media Player', the virtual ones don't work?
    return [device for device in devices
            if device.model_description == 'Digital Media Player']


class RaumfeldDevice(object):

    def __init__(self, location):
        self.location = location

        # parse location url
        scheme, netloc, path, _, _, _ = urlparse.urlparse(location)
        self.address = '%s://%s' % (scheme, netloc)
        self._parse_device_description()

        # set up soap clients
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

    def _parse_device_description(self):
        http = (get_Http())()
        xml = fetch(self.location, http)
        d = SimpleXMLElement(xml)
        self.friendly_name = str(next(d.device.friendlyName()))
        self.model_description = str(next(d.device.modelDescription()))
        self.model_name = str(next(d.modelName()))

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
        self.rendering_control.SetMute(InstanceID=1,
                                       DesiredMute=1 if mute else 0)

    def __repr__(self):
        return ("<RaumfeldDevice (%s, %s, %s)>" %
               (self.friendly_name, self.model_name, self.model_description))


if __name__ == '__main__':
    devices = discover()
    print devices

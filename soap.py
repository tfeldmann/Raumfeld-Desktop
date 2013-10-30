from pysimplesoap.client import SoapClient

rendering_control = SoapClient(
    location="http://192.168.178.37:56694/RenderingService/Control",
    action="urn:upnp-org:serviceId:RenderingControl#",
    namespace="http://schemas.xmlsoap.org/soap/envelope/",
    soap_ns='soap', ns='s', exceptions=True)

av_transport = SoapClient(
    location="http://192.168.178.37:56694/TransportService/Control",
    action="urn:schemas-upnp-org:service:AVTransport:1#",
    namespace="http://schemas.xmlsoap.org/soap/envelope/",
    soap_ns='soap', ns='s', exceptions=True)

# response = client.Play(InstanceID=1, Speed=2)
# response = client.Pause(InstanceID=1)
# response = av_transport.Play(InstanceID=1)
# response = rendering_control.SetVolume(InstanceID=1, DesiredVolume=0)
# response = rendering_control.SetMute(InstanceID=1, DesiredMute=0)

response = rendering_control.GetVolume(InstanceID=1)
print response.CurrentVolume

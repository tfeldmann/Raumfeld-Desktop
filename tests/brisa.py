from brisa.core.reactors import install_default_reactor
reactor = install_default_reactor()
from brisa.core.network import parse_url
from brisa.core.threaded_call import run_async_function
from brisa.upnp.control_point.control_point import ControlPoint

def on_new_device(dev):
    if not dev:
        return
    print 'Got new device:', dev.udn
    print "Type list to see the whole list"


c = ControlPoint()
c.subscribe('new_device_event', on_new_device)

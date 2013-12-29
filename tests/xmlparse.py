from pysimplesoap.simplexml import SimpleXMLElement
xml = """<?xml version="1.0" encoding="utf-8"?>
<root xmlns="urn:schemas-upnp-org:device-1-0" xmlns:raumfeld="urn:schemas-raumfeld-com:device">
    <specVersion>
        <major>1</major>
        <minor>0</minor>
    </specVersion>
    <device>
        <deviceType>urn:schemas-upnp-org:device:MediaRenderer:1</deviceType>
        <X_DLNACAP>playcontainer-0-1</X_DLNACAP>
        <friendlyName>Wohnzimmer</friendlyName>
        <modelDescription>Virtual Media Player</modelDescription>
        <modelName>Raumfeld One</modelName>
        <UDN>uuid:2267B032-35FF-40E9-BC45-8DB8927BBE8B</UDN>
        <iconList>
            <icon>
                <mimetype>image/png</mimetype>
                <width>48</width>
                <height>48</height>
                <depth>24</depth>
                <url>/icons/raumfeld-48.png</url>
            </icon>
            <icon>
                <mimetype>image/png</mimetype>
                <width>32</width>
                <height>32</height>
                <depth>24</depth>
                <url>/icons/raumfeld-32.png</url>
            </icon>
        </iconList>
        <serviceList>
            <service>
                <serviceType>urn:schemas-upnp-org:service:RenderingControl:1</serviceType>
                <serviceId>urn:upnp-org:serviceId:RenderingControl</serviceId>
                <SCPDURL>/RenderingService.xml</SCPDURL>
                <controlURL>/RenderingService/Control</controlURL>
                <eventSubURL>/RenderingService/Event</eventSubURL>
            </service>
            <service>
                <serviceType>urn:schemas-upnp-org:service:AVTransport:1</serviceType>
                <serviceId>urn:upnp-org:serviceId:AVTransport</serviceId>
                <SCPDURL>TransportService.xml</SCPDURL>
                <controlURL>/TransportService/Control</controlURL>
                <eventSubURL>/TransportService/Event</eventSubURL>
            </service>
            <service>
                <serviceType>urn:schemas-upnp-org:service:ConnectionManager:1</serviceType>
                <serviceId>urn:upnp-org:serviceId:ConnectionManager</serviceId>
                <SCPDURL>ConnectionManager.xml</SCPDURL>
                <controlURL>/ConnectionManager/Control</controlURL>
                <eventSubURL>/ConnectionManager/Event</eventSubURL>
            </service>
        </serviceList>
        <manufacturer>Raumfeld GmbH</manufacturer>
        <manufacturerURL>http://www.raumfeld.com/</manufacturerURL>
        <presentationURL>Welcome</presentationURL>
        <modelNumber>1</modelNumber>
        <serialNumber>00:26:06:19:1f:82</serialNumber>
        <raumfeld:protocolVersion>47</raumfeld:protocolVersion>
    </device>
</root>
"""
e = SimpleXMLElement(xml)
friendly_name = str(next(e.device.friendlyName()))
model_description = str(next(e.device.modelDescription()))
model_name = str(next(e.modelName()))

# MIT LICENSE
#
# Copyright 1997 - 2020 by IXIA Keysight
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE. 
from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class MatchMask(Base):
    """Select the type of match mask capability that the table will support.
    The MatchMask class encapsulates a required matchMask resource which will be retrieved from the server every time the property is accessed.
    """

    __slots__ = ()
    _SDM_NAME = 'matchMask'
    _SDM_ATT_MAP = {
        'ArpDestinationIpv4AddressMask': 'arpDestinationIpv4AddressMask',
        'ArpDstHwAddressMask': 'arpDstHwAddressMask',
        'ArpSourceIpv4AddressMask': 'arpSourceIpv4AddressMask',
        'ArpSrcHwAddressMask': 'arpSrcHwAddressMask',
        'EthernetDestinationMask': 'ethernetDestinationMask',
        'EthernetSourceMask': 'ethernetSourceMask',
        'Ipv4DestinationMask': 'ipv4DestinationMask',
        'Ipv4SourceMask': 'ipv4SourceMask',
        'Ipv6DestinationMask': 'ipv6DestinationMask',
        'Ipv6ExtHeaderMask': 'ipv6ExtHeaderMask',
        'Ipv6FlowLabelMask': 'ipv6FlowLabelMask',
        'Ipv6SourceMask': 'ipv6SourceMask',
        'MetadataMask': 'metadataMask',
        'PbbIsidMask': 'pbbIsidMask',
        'TunnelIdMask': 'tunnelIdMask',
        'VlanMask': 'vlanMask',
    }

    def __init__(self, parent):
        super(MatchMask, self).__init__(parent)

    @property
    def ArpDestinationIpv4AddressMask(self):
        """
        Returns
        -------
        - bool: If selected, ARP Destination IPv4 Address Mask matching is supported.
        """
        return self._get_attribute(self._SDM_ATT_MAP['ArpDestinationIpv4AddressMask'])
    @ArpDestinationIpv4AddressMask.setter
    def ArpDestinationIpv4AddressMask(self, value):
        self._set_attribute(self._SDM_ATT_MAP['ArpDestinationIpv4AddressMask'], value)

    @property
    def ArpDstHwAddressMask(self):
        """
        Returns
        -------
        - bool: If selected, ARP Destination Hardware Address Mask matching is supported.
        """
        return self._get_attribute(self._SDM_ATT_MAP['ArpDstHwAddressMask'])
    @ArpDstHwAddressMask.setter
    def ArpDstHwAddressMask(self, value):
        self._set_attribute(self._SDM_ATT_MAP['ArpDstHwAddressMask'], value)

    @property
    def ArpSourceIpv4AddressMask(self):
        """
        Returns
        -------
        - bool: If selected, ARP Source IPv4 Address Mask matching is supported.
        """
        return self._get_attribute(self._SDM_ATT_MAP['ArpSourceIpv4AddressMask'])
    @ArpSourceIpv4AddressMask.setter
    def ArpSourceIpv4AddressMask(self, value):
        self._set_attribute(self._SDM_ATT_MAP['ArpSourceIpv4AddressMask'], value)

    @property
    def ArpSrcHwAddressMask(self):
        """
        Returns
        -------
        - bool: If selected, ARP Source Hardware Address Mask matching is supported.
        """
        return self._get_attribute(self._SDM_ATT_MAP['ArpSrcHwAddressMask'])
    @ArpSrcHwAddressMask.setter
    def ArpSrcHwAddressMask(self, value):
        self._set_attribute(self._SDM_ATT_MAP['ArpSrcHwAddressMask'], value)

    @property
    def EthernetDestinationMask(self):
        """
        Returns
        -------
        - bool: If selected, Ethernet Destination Mask matching is supported.
        """
        return self._get_attribute(self._SDM_ATT_MAP['EthernetDestinationMask'])
    @EthernetDestinationMask.setter
    def EthernetDestinationMask(self, value):
        self._set_attribute(self._SDM_ATT_MAP['EthernetDestinationMask'], value)

    @property
    def EthernetSourceMask(self):
        """
        Returns
        -------
        - bool: If selected, Ethernet Source Mask matching is supported.
        """
        return self._get_attribute(self._SDM_ATT_MAP['EthernetSourceMask'])
    @EthernetSourceMask.setter
    def EthernetSourceMask(self, value):
        self._set_attribute(self._SDM_ATT_MAP['EthernetSourceMask'], value)

    @property
    def Ipv4DestinationMask(self):
        """
        Returns
        -------
        - bool: If selected, IPv4 Destination Mask matching is supported.
        """
        return self._get_attribute(self._SDM_ATT_MAP['Ipv4DestinationMask'])
    @Ipv4DestinationMask.setter
    def Ipv4DestinationMask(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Ipv4DestinationMask'], value)

    @property
    def Ipv4SourceMask(self):
        """
        Returns
        -------
        - bool: If selected, IPv4 Source Mask matching is supported.
        """
        return self._get_attribute(self._SDM_ATT_MAP['Ipv4SourceMask'])
    @Ipv4SourceMask.setter
    def Ipv4SourceMask(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Ipv4SourceMask'], value)

    @property
    def Ipv6DestinationMask(self):
        """
        Returns
        -------
        - bool: If selected, IPv6 Destination Mask matching is supported.
        """
        return self._get_attribute(self._SDM_ATT_MAP['Ipv6DestinationMask'])
    @Ipv6DestinationMask.setter
    def Ipv6DestinationMask(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Ipv6DestinationMask'], value)

    @property
    def Ipv6ExtHeaderMask(self):
        """
        Returns
        -------
        - bool: If selected, IPv6 Ext Header Mask matching is supported.
        """
        return self._get_attribute(self._SDM_ATT_MAP['Ipv6ExtHeaderMask'])
    @Ipv6ExtHeaderMask.setter
    def Ipv6ExtHeaderMask(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Ipv6ExtHeaderMask'], value)

    @property
    def Ipv6FlowLabelMask(self):
        """
        Returns
        -------
        - bool: If selected, IPv6 Flow Label Mask matching is supported.
        """
        return self._get_attribute(self._SDM_ATT_MAP['Ipv6FlowLabelMask'])
    @Ipv6FlowLabelMask.setter
    def Ipv6FlowLabelMask(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Ipv6FlowLabelMask'], value)

    @property
    def Ipv6SourceMask(self):
        """
        Returns
        -------
        - bool: If selected, IPv6 Source Mask matching is supported.
        """
        return self._get_attribute(self._SDM_ATT_MAP['Ipv6SourceMask'])
    @Ipv6SourceMask.setter
    def Ipv6SourceMask(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Ipv6SourceMask'], value)

    @property
    def MetadataMask(self):
        """
        Returns
        -------
        - bool: If selected, MetaData Mask matching is supported.
        """
        return self._get_attribute(self._SDM_ATT_MAP['MetadataMask'])
    @MetadataMask.setter
    def MetadataMask(self, value):
        self._set_attribute(self._SDM_ATT_MAP['MetadataMask'], value)

    @property
    def PbbIsidMask(self):
        """
        Returns
        -------
        - bool: If selected, Tunnel ID Mask matching is supported.
        """
        return self._get_attribute(self._SDM_ATT_MAP['PbbIsidMask'])
    @PbbIsidMask.setter
    def PbbIsidMask(self, value):
        self._set_attribute(self._SDM_ATT_MAP['PbbIsidMask'], value)

    @property
    def TunnelIdMask(self):
        """
        Returns
        -------
        - bool: If selected, Tunnel ID Mask matching is supported.
        """
        return self._get_attribute(self._SDM_ATT_MAP['TunnelIdMask'])
    @TunnelIdMask.setter
    def TunnelIdMask(self, value):
        self._set_attribute(self._SDM_ATT_MAP['TunnelIdMask'], value)

    @property
    def VlanMask(self):
        """
        Returns
        -------
        - bool: If selected, VLAN Mask matching is supported.
        """
        return self._get_attribute(self._SDM_ATT_MAP['VlanMask'])
    @VlanMask.setter
    def VlanMask(self, value):
        self._set_attribute(self._SDM_ATT_MAP['VlanMask'], value)

    def update(self, ArpDestinationIpv4AddressMask=None, ArpDstHwAddressMask=None, ArpSourceIpv4AddressMask=None, ArpSrcHwAddressMask=None, EthernetDestinationMask=None, EthernetSourceMask=None, Ipv4DestinationMask=None, Ipv4SourceMask=None, Ipv6DestinationMask=None, Ipv6ExtHeaderMask=None, Ipv6FlowLabelMask=None, Ipv6SourceMask=None, MetadataMask=None, PbbIsidMask=None, TunnelIdMask=None, VlanMask=None):
        """Updates matchMask resource on the server.

        Args
        ----
        - ArpDestinationIpv4AddressMask (bool): If selected, ARP Destination IPv4 Address Mask matching is supported.
        - ArpDstHwAddressMask (bool): If selected, ARP Destination Hardware Address Mask matching is supported.
        - ArpSourceIpv4AddressMask (bool): If selected, ARP Source IPv4 Address Mask matching is supported.
        - ArpSrcHwAddressMask (bool): If selected, ARP Source Hardware Address Mask matching is supported.
        - EthernetDestinationMask (bool): If selected, Ethernet Destination Mask matching is supported.
        - EthernetSourceMask (bool): If selected, Ethernet Source Mask matching is supported.
        - Ipv4DestinationMask (bool): If selected, IPv4 Destination Mask matching is supported.
        - Ipv4SourceMask (bool): If selected, IPv4 Source Mask matching is supported.
        - Ipv6DestinationMask (bool): If selected, IPv6 Destination Mask matching is supported.
        - Ipv6ExtHeaderMask (bool): If selected, IPv6 Ext Header Mask matching is supported.
        - Ipv6FlowLabelMask (bool): If selected, IPv6 Flow Label Mask matching is supported.
        - Ipv6SourceMask (bool): If selected, IPv6 Source Mask matching is supported.
        - MetadataMask (bool): If selected, MetaData Mask matching is supported.
        - PbbIsidMask (bool): If selected, Tunnel ID Mask matching is supported.
        - TunnelIdMask (bool): If selected, Tunnel ID Mask matching is supported.
        - VlanMask (bool): If selected, VLAN Mask matching is supported.

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._update(self._map_locals(self._SDM_ATT_MAP, locals()))

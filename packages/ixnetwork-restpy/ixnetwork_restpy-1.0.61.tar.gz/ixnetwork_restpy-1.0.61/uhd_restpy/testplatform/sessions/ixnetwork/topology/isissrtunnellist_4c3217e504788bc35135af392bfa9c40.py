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
from uhd_restpy.base import Base
from uhd_restpy.files import Files


class IsisSRTunnelList(Base):
    """ISIS MPLS SR Tunnel
    The IsisSRTunnelList class encapsulates a required isisSRTunnelList resource which will be retrieved from the server every time the property is accessed.
    """

    __slots__ = ()
    _SDM_NAME = 'isisSRTunnelList'
    _SDM_ATT_MAP = {
        'Active': 'active',
        'Count': 'count',
        'DescriptiveName': 'descriptiveName',
        'Name': 'name',
        'NumberOfSegments': 'numberOfSegments',
        'SourceIpv4': 'sourceIpv4',
        'SourceIpv6': 'sourceIpv6',
        'TunnelDescription': 'tunnelDescription',
        'UsingHeadEndNodePrefix': 'usingHeadEndNodePrefix',
    }

    def __init__(self, parent):
        super(IsisSRTunnelList, self).__init__(parent)

    @property
    def IsisSegmentList(self):
        """
        Returns
        -------
        - obj(uhd_restpy.testplatform.sessions.ixnetwork.topology.isissegmentlist_28066a67f7cf6594d73c8fed733b33f6.IsisSegmentList): An instance of the IsisSegmentList class

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        from uhd_restpy.testplatform.sessions.ixnetwork.topology.isissegmentlist_28066a67f7cf6594d73c8fed733b33f6 import IsisSegmentList
        return IsisSegmentList(self)

    @property
    def Tag(self):
        """
        Returns
        -------
        - obj(uhd_restpy.testplatform.sessions.ixnetwork.topology.tag_e30f24de79247381d4dfd423b2f6986d.Tag): An instance of the Tag class

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        from uhd_restpy.testplatform.sessions.ixnetwork.topology.tag_e30f24de79247381d4dfd423b2f6986d import Tag
        return Tag(self)

    @property
    def Active(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Activate/Deactivate Configuration.
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['Active']))

    @property
    def Count(self):
        """
        Returns
        -------
        - number: Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group.
        """
        return self._get_attribute(self._SDM_ATT_MAP['Count'])

    @property
    def DescriptiveName(self):
        """
        Returns
        -------
        - str: Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but may offer more context.
        """
        return self._get_attribute(self._SDM_ATT_MAP['DescriptiveName'])

    @property
    def Name(self):
        """
        Returns
        -------
        - str: Name of NGPF element, guaranteed to be unique in Scenario
        """
        return self._get_attribute(self._SDM_ATT_MAP['Name'])
    @Name.setter
    def Name(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Name'], value)

    @property
    def NumberOfSegments(self):
        """
        Returns
        -------
        - number: Number of Segments
        """
        return self._get_attribute(self._SDM_ATT_MAP['NumberOfSegments'])
    @NumberOfSegments.setter
    def NumberOfSegments(self, value):
        self._set_attribute(self._SDM_ATT_MAP['NumberOfSegments'], value)

    @property
    def SourceIpv4(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Source IPv4
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['SourceIpv4']))

    @property
    def SourceIpv6(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Source IPv6
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['SourceIpv6']))

    @property
    def TunnelDescription(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Tunnel Description
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['TunnelDescription']))

    @property
    def UsingHeadEndNodePrefix(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Using head end Node prefix
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['UsingHeadEndNodePrefix']))

    def update(self, Name=None, NumberOfSegments=None):
        """Updates isisSRTunnelList resource on the server.

        This method has some named parameters with a type: obj (Multivalue).
        The Multivalue class has documentation that details the possible values for those named parameters.

        Args
        ----
        - Name (str): Name of NGPF element, guaranteed to be unique in Scenario
        - NumberOfSegments (number): Number of Segments

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._update(self._map_locals(self._SDM_ATT_MAP, locals()))

    def get_device_ids(self, PortNames=None, Active=None, SourceIpv4=None, SourceIpv6=None, TunnelDescription=None, UsingHeadEndNodePrefix=None):
        """Base class infrastructure that gets a list of isisSRTunnelList device ids encapsulated by this object.

        Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

        Args
        ----
        - PortNames (str): optional regex of port names
        - Active (str): optional regex of active
        - SourceIpv4 (str): optional regex of sourceIpv4
        - SourceIpv6 (str): optional regex of sourceIpv6
        - TunnelDescription (str): optional regex of tunnelDescription
        - UsingHeadEndNodePrefix (str): optional regex of usingHeadEndNodePrefix

        Returns
        -------
        - list(int): A list of device ids that meets the regex criteria provided in the method parameters

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._get_ngpf_device_ids(locals())

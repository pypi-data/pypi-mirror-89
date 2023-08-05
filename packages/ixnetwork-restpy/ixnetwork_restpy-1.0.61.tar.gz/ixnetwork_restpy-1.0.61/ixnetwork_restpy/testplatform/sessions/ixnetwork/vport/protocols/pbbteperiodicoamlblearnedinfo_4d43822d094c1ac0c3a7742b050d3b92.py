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


class PbbTePeriodicOamLbLearnedInfo(Base):
    """The ppbTePeriodicOamLtLearnedInfo object holds the PBB-TE periodic OAM loopback learned information.
    The PbbTePeriodicOamLbLearnedInfo class encapsulates a list of pbbTePeriodicOamLbLearnedInfo resources that are managed by the system.
    A list of resources can be retrieved from the server using the PbbTePeriodicOamLbLearnedInfo.find() method.
    """

    __slots__ = ()
    _SDM_NAME = 'pbbTePeriodicOamLbLearnedInfo'
    _SDM_ATT_MAP = {
        'AverageRtt': 'averageRtt',
        'BVlan': 'bVlan',
        'DstMacAddress': 'dstMacAddress',
        'LbmSentCount': 'lbmSentCount',
        'MdLevel': 'mdLevel',
        'NoReplyCount': 'noReplyCount',
        'RecentReachability': 'recentReachability',
        'RecentRtt': 'recentRtt',
        'SrcMacAddress': 'srcMacAddress',
    }

    def __init__(self, parent):
        super(PbbTePeriodicOamLbLearnedInfo, self).__init__(parent)

    @property
    def AverageRtt(self):
        """
        Returns
        -------
        - number: (read only) The learned average periodic OAM Round-Trip-Time.
        """
        return self._get_attribute(self._SDM_ATT_MAP['AverageRtt'])

    @property
    def BVlan(self):
        """
        Returns
        -------
        - str: (read only) The learned periodic OAM B-VLAN identifier.
        """
        return self._get_attribute(self._SDM_ATT_MAP['BVlan'])

    @property
    def DstMacAddress(self):
        """
        Returns
        -------
        - str: (read only) The learned periodic OAM destination MAC address.
        """
        return self._get_attribute(self._SDM_ATT_MAP['DstMacAddress'])

    @property
    def LbmSentCount(self):
        """
        Returns
        -------
        - number: (read only) The learned number of periodic OAM loopback messages sent.
        """
        return self._get_attribute(self._SDM_ATT_MAP['LbmSentCount'])

    @property
    def MdLevel(self):
        """
        Returns
        -------
        - number: (read only) The learned MD level for the periodic OAM.
        """
        return self._get_attribute(self._SDM_ATT_MAP['MdLevel'])

    @property
    def NoReplyCount(self):
        """
        Returns
        -------
        - number: (read only) The learned number of periodic OAM no replies.
        """
        return self._get_attribute(self._SDM_ATT_MAP['NoReplyCount'])

    @property
    def RecentReachability(self):
        """
        Returns
        -------
        - bool: (read only) Indicates the status of the Ping.
        """
        return self._get_attribute(self._SDM_ATT_MAP['RecentReachability'])

    @property
    def RecentRtt(self):
        """
        Returns
        -------
        - number: (read only) Indicates the status of the round-trip-time
        """
        return self._get_attribute(self._SDM_ATT_MAP['RecentRtt'])

    @property
    def SrcMacAddress(self):
        """
        Returns
        -------
        - str: (read only) The learned periodic OAM source MAC address.
        """
        return self._get_attribute(self._SDM_ATT_MAP['SrcMacAddress'])

    def find(self, AverageRtt=None, BVlan=None, DstMacAddress=None, LbmSentCount=None, MdLevel=None, NoReplyCount=None, RecentReachability=None, RecentRtt=None, SrcMacAddress=None):
        """Finds and retrieves pbbTePeriodicOamLbLearnedInfo resources from the server.

        All named parameters are evaluated on the server using regex. The named parameters can be used to selectively retrieve pbbTePeriodicOamLbLearnedInfo resources from the server.
        To retrieve an exact match ensure the parameter value starts with ^ and ends with $
        By default the find method takes no parameters and will retrieve all pbbTePeriodicOamLbLearnedInfo resources from the server.

        Args
        ----
        - AverageRtt (number): (read only) The learned average periodic OAM Round-Trip-Time.
        - BVlan (str): (read only) The learned periodic OAM B-VLAN identifier.
        - DstMacAddress (str): (read only) The learned periodic OAM destination MAC address.
        - LbmSentCount (number): (read only) The learned number of periodic OAM loopback messages sent.
        - MdLevel (number): (read only) The learned MD level for the periodic OAM.
        - NoReplyCount (number): (read only) The learned number of periodic OAM no replies.
        - RecentReachability (bool): (read only) Indicates the status of the Ping.
        - RecentRtt (number): (read only) Indicates the status of the round-trip-time
        - SrcMacAddress (str): (read only) The learned periodic OAM source MAC address.

        Returns
        -------
        - self: This instance with matching pbbTePeriodicOamLbLearnedInfo resources retrieved from the server available through an iterator or index

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(self._map_locals(self._SDM_ATT_MAP, locals()))

    def read(self, href):
        """Retrieves a single instance of pbbTePeriodicOamLbLearnedInfo data from the server.

        Args
        ----
        - href (str): An href to the instance to be retrieved

        Returns
        -------
        - self: This instance with the pbbTePeriodicOamLbLearnedInfo resources from the server available through an iterator or index

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)

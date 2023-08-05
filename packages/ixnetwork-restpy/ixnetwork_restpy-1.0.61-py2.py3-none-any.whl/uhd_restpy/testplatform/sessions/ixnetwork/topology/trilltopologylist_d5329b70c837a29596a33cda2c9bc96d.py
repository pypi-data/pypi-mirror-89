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


class TrillTopologyList(Base):
    """TRILL Topology
    The TrillTopologyList class encapsulates a required trillTopologyList resource which will be retrieved from the server every time the property is accessed.
    """

    __slots__ = ()
    _SDM_NAME = 'trillTopologyList'
    _SDM_ATT_MAP = {
        'Active': 'active',
        'Count': 'count',
        'DescriptiveName': 'descriptiveName',
        'InterestedVlanRangeCount': 'interestedVlanRangeCount',
        'LocalSystemID': 'localSystemID',
        'Name': 'name',
        'NicknameCount': 'nicknameCount',
        'NoOfTreesToCompute': 'noOfTreesToCompute',
        'TopologyId': 'topologyId',
    }

    def __init__(self, parent):
        super(TrillTopologyList, self).__init__(parent)

    @property
    def InterestedVlanList(self):
        """
        Returns
        -------
        - obj(uhd_restpy.testplatform.sessions.ixnetwork.topology.interestedvlanlist_73520df8ad4853f551ecc4bd98996b9f.InterestedVlanList): An instance of the InterestedVlanList class

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        from uhd_restpy.testplatform.sessions.ixnetwork.topology.interestedvlanlist_73520df8ad4853f551ecc4bd98996b9f import InterestedVlanList
        return InterestedVlanList(self)._select()

    @property
    def NicknameRecordList(self):
        """
        Returns
        -------
        - obj(uhd_restpy.testplatform.sessions.ixnetwork.topology.nicknamerecordlist_5633e9074910fb78b98b5edd7b09d613.NicknameRecordList): An instance of the NicknameRecordList class

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        from uhd_restpy.testplatform.sessions.ixnetwork.topology.nicknamerecordlist_5633e9074910fb78b98b5edd7b09d613 import NicknameRecordList
        return NicknameRecordList(self)._select()

    @property
    def Active(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Activate/Deactivate Configuration
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
        - str: Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but may offers more context
        """
        return self._get_attribute(self._SDM_ATT_MAP['DescriptiveName'])

    @property
    def InterestedVlanRangeCount(self):
        """
        Returns
        -------
        - number: Interested VLAN Range Count(multiplier)
        """
        return self._get_attribute(self._SDM_ATT_MAP['InterestedVlanRangeCount'])
    @InterestedVlanRangeCount.setter
    def InterestedVlanRangeCount(self, value):
        self._set_attribute(self._SDM_ATT_MAP['InterestedVlanRangeCount'], value)

    @property
    def LocalSystemID(self):
        """
        Returns
        -------
        - list(str): System ID
        """
        return self._get_attribute(self._SDM_ATT_MAP['LocalSystemID'])

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
    def NicknameCount(self):
        """
        Returns
        -------
        - number: Nickname Count(multiplier)
        """
        return self._get_attribute(self._SDM_ATT_MAP['NicknameCount'])
    @NicknameCount.setter
    def NicknameCount(self, value):
        self._set_attribute(self._SDM_ATT_MAP['NicknameCount'], value)

    @property
    def NoOfTreesToCompute(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): No. of Trees to Compute
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['NoOfTreesToCompute']))

    @property
    def TopologyId(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Topology Id
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['TopologyId']))

    def update(self, InterestedVlanRangeCount=None, Name=None, NicknameCount=None):
        """Updates trillTopologyList resource on the server.

        This method has some named parameters with a type: obj (Multivalue).
        The Multivalue class has documentation that details the possible values for those named parameters.

        Args
        ----
        - InterestedVlanRangeCount (number): Interested VLAN Range Count(multiplier)
        - Name (str): Name of NGPF element, guaranteed to be unique in Scenario
        - NicknameCount (number): Nickname Count(multiplier)

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._update(self._map_locals(self._SDM_ATT_MAP, locals()))

    def get_device_ids(self, PortNames=None, Active=None, NoOfTreesToCompute=None, TopologyId=None):
        """Base class infrastructure that gets a list of trillTopologyList device ids encapsulated by this object.

        Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

        Args
        ----
        - PortNames (str): optional regex of port names
        - Active (str): optional regex of active
        - NoOfTreesToCompute (str): optional regex of noOfTreesToCompute
        - TopologyId (str): optional regex of topologyId

        Returns
        -------
        - list(int): A list of device ids that meets the regex criteria provided in the method parameters

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._get_ngpf_device_ids(locals())

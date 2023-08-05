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


class LinkLsaRoutes(Base):
    """Link Lsa routes
    The LinkLsaRoutes class encapsulates a list of linkLsaRoutes resources that are managed by the system.
    A list of resources can be retrieved from the server using the LinkLsaRoutes.find() method.
    """

    __slots__ = ()
    _SDM_NAME = 'linkLsaRoutes'
    _SDM_ATT_MAP = {
        'Active': 'active',
        'Count': 'count',
        'DCBit': 'dCBit',
        'DescriptiveName': 'descriptiveName',
        'EBit': 'eBit',
        'LABit': 'lABit',
        'LinkLocalAddress': 'linkLocalAddress',
        'LinkStateId': 'linkStateId',
        'LinkStateIdStep': 'linkStateIdStep',
        'MCBit': 'mCBit',
        'Metric': 'metric',
        'NBit': 'nBit',
        'NUBit': 'nUBit',
        'Name': 'name',
        'NetworkAddress': 'networkAddress',
        'PBit': 'pBit',
        'Prefix': 'prefix',
        'RBit': 'rBit',
        'RangeSize': 'rangeSize',
        'ReservedBit6': 'reservedBit6',
        'ReservedBit7': 'reservedBit7',
        'RouterPriority': 'routerPriority',
        'UnusedBit4': 'unusedBit4',
        'UnusedBit5': 'unusedBit5',
        'UnusedBit6': 'unusedBit6',
        'UnusedBit7': 'unusedBit7',
        'V6Bit': 'v6Bit',
        'XBit': 'xBit',
    }

    def __init__(self, parent):
        super(LinkLsaRoutes, self).__init__(parent)

    @property
    def Active(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Whether this is to be advertised or not
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
    def DCBit(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Demand Circuit bit
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['DCBit']))

    @property
    def DescriptiveName(self):
        """
        Returns
        -------
        - str: Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but may offers more context
        """
        return self._get_attribute(self._SDM_ATT_MAP['DescriptiveName'])

    @property
    def EBit(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): bit describing how AS-external-LSAs are flooded
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['EBit']))

    @property
    def LABit(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Options-LA Bit(Local Address)
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['LABit']))

    @property
    def LinkLocalAddress(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): 128 Bits IPv6 address.
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['LinkLocalAddress']))

    @property
    def LinkStateId(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Link State Id of the simulated IPv6 network
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['LinkStateId']))

    @property
    def LinkStateIdStep(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Link State Id Step for the LSAs to be generated for this set of IPv6 Inter-Area networks.
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['LinkStateIdStep']))

    @property
    def MCBit(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Options-MC Bit(Multicast)
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['MCBit']))

    @property
    def Metric(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Metric
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['Metric']))

    @property
    def NBit(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): bit for handling Type 7 LSAs
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['NBit']))

    @property
    def NUBit(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Options-NU Bit(No Unicast)
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['NUBit']))

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
    def NetworkAddress(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Prefixes of the simulated IPv6 network
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['NetworkAddress']))

    @property
    def PBit(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Options-P Bit(Propagate)
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['PBit']))

    @property
    def Prefix(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Prefix Length
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['Prefix']))

    @property
    def RBit(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Router bit
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['RBit']))

    @property
    def RangeSize(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Range Size
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['RangeSize']))

    @property
    def ReservedBit6(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): (6) Reserved Bit
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['ReservedBit6']))

    @property
    def ReservedBit7(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): (7) Reserved Bit
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['ReservedBit7']))

    @property
    def RouterPriority(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Router Priority
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['RouterPriority']))

    @property
    def UnusedBit4(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Options-(4)Unused
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['UnusedBit4']))

    @property
    def UnusedBit5(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Options-(5)Unused
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['UnusedBit5']))

    @property
    def UnusedBit6(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Options-(6)Unused
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['UnusedBit6']))

    @property
    def UnusedBit7(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Options-(7)Unused
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['UnusedBit7']))

    @property
    def V6Bit(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): bit for excluding the router/link from IPv6 routing calculations. If clear, router/link is excluded
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['V6Bit']))

    @property
    def XBit(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): bit for forwarding of IP multicast datagrams
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['XBit']))

    def update(self, Name=None):
        """Updates linkLsaRoutes resource on the server.

        This method has some named parameters with a type: obj (Multivalue).
        The Multivalue class has documentation that details the possible values for those named parameters.

        Args
        ----
        - Name (str): Name of NGPF element, guaranteed to be unique in Scenario

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._update(self._map_locals(self._SDM_ATT_MAP, locals()))

    def find(self, Count=None, DescriptiveName=None, Name=None):
        """Finds and retrieves linkLsaRoutes resources from the server.

        All named parameters are evaluated on the server using regex. The named parameters can be used to selectively retrieve linkLsaRoutes resources from the server.
        To retrieve an exact match ensure the parameter value starts with ^ and ends with $
        By default the find method takes no parameters and will retrieve all linkLsaRoutes resources from the server.

        Args
        ----
        - Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group.
        - DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but may offers more context
        - Name (str): Name of NGPF element, guaranteed to be unique in Scenario

        Returns
        -------
        - self: This instance with matching linkLsaRoutes resources retrieved from the server available through an iterator or index

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(self._map_locals(self._SDM_ATT_MAP, locals()))

    def read(self, href):
        """Retrieves a single instance of linkLsaRoutes data from the server.

        Args
        ----
        - href (str): An href to the instance to be retrieved

        Returns
        -------
        - self: This instance with the linkLsaRoutes resources from the server available through an iterator or index

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)

    def get_device_ids(self, PortNames=None, Active=None, DCBit=None, EBit=None, LABit=None, LinkLocalAddress=None, LinkStateId=None, LinkStateIdStep=None, MCBit=None, Metric=None, NBit=None, NUBit=None, NetworkAddress=None, PBit=None, Prefix=None, RBit=None, RangeSize=None, ReservedBit6=None, ReservedBit7=None, RouterPriority=None, UnusedBit4=None, UnusedBit5=None, UnusedBit6=None, UnusedBit7=None, V6Bit=None, XBit=None):
        """Base class infrastructure that gets a list of linkLsaRoutes device ids encapsulated by this object.

        Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

        Args
        ----
        - PortNames (str): optional regex of port names
        - Active (str): optional regex of active
        - DCBit (str): optional regex of dCBit
        - EBit (str): optional regex of eBit
        - LABit (str): optional regex of lABit
        - LinkLocalAddress (str): optional regex of linkLocalAddress
        - LinkStateId (str): optional regex of linkStateId
        - LinkStateIdStep (str): optional regex of linkStateIdStep
        - MCBit (str): optional regex of mCBit
        - Metric (str): optional regex of metric
        - NBit (str): optional regex of nBit
        - NUBit (str): optional regex of nUBit
        - NetworkAddress (str): optional regex of networkAddress
        - PBit (str): optional regex of pBit
        - Prefix (str): optional regex of prefix
        - RBit (str): optional regex of rBit
        - RangeSize (str): optional regex of rangeSize
        - ReservedBit6 (str): optional regex of reservedBit6
        - ReservedBit7 (str): optional regex of reservedBit7
        - RouterPriority (str): optional regex of routerPriority
        - UnusedBit4 (str): optional regex of unusedBit4
        - UnusedBit5 (str): optional regex of unusedBit5
        - UnusedBit6 (str): optional regex of unusedBit6
        - UnusedBit7 (str): optional regex of unusedBit7
        - V6Bit (str): optional regex of v6Bit
        - XBit (str): optional regex of xBit

        Returns
        -------
        - list(int): A list of device ids that meets the regex criteria provided in the method parameters

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._get_ngpf_device_ids(locals())

    def Advertise(self, *args, **kwargs):
        """Executes the advertise operation on the server.

        Advertise selected routes

        The IxNetwork model allows for multiple method Signatures with the same name while python does not.

        advertise(SessionIndices=list)
        ------------------------------
        - SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        advertise(SessionIndices=string)
        --------------------------------
        - SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('advertise', payload=payload, response_object=None)

    def Start(self):
        """Executes the start operation on the server.

        Start CPF control plane (equals to promote to negotiated state).

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        return self._execute('start', payload=payload, response_object=None)

    def Stop(self):
        """Executes the stop operation on the server.

        Stop CPF control plane (equals to demote to PreValidated-DoDDone state).

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        return self._execute('stop', payload=payload, response_object=None)

    def Withdraw(self, *args, **kwargs):
        """Executes the withdraw operation on the server.

        Withdraw selected routes

        The IxNetwork model allows for multiple method Signatures with the same name while python does not.

        withdraw(SessionIndices=list)
        -----------------------------
        - SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        withdraw(SessionIndices=string)
        -------------------------------
        - SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('withdraw', payload=payload, response_object=None)

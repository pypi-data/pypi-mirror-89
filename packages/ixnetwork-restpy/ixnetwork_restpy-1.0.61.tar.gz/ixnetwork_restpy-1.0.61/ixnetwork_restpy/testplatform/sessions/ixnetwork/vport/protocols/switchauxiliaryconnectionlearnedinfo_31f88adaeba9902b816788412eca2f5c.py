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


class SwitchAuxiliaryConnectionLearnedInfo(Base):
    """This object allows to configure the switch auxiliary connection learned information.
    The SwitchAuxiliaryConnectionLearnedInfo class encapsulates a list of switchAuxiliaryConnectionLearnedInfo resources that are managed by the system.
    A list of resources can be retrieved from the server using the SwitchAuxiliaryConnectionLearnedInfo.find() method.
    """

    __slots__ = ()
    _SDM_NAME = 'switchAuxiliaryConnectionLearnedInfo'
    _SDM_ATT_MAP = {
        'AuxiliaryId': 'auxiliaryId',
        'ConnectionType': 'connectionType',
        'DataPathId': 'dataPathId',
        'DataPathIdAsHex': 'dataPathIdAsHex',
        'LocalIp': 'localIp',
        'LocalPort': 'localPort',
        'RemoteIp': 'remoteIp',
        'RemotePort': 'remotePort',
    }

    def __init__(self, parent):
        super(SwitchAuxiliaryConnectionLearnedInfo, self).__init__(parent)

    @property
    def AuxiliaryId(self):
        """
        Returns
        -------
        - number: This describes the identifier for auxiliary connections.
        """
        return self._get_attribute(self._SDM_ATT_MAP['AuxiliaryId'])

    @property
    def ConnectionType(self):
        """
        Returns
        -------
        - str(tcp | tls | udp): This describes the type of OpenFlow connection.
        """
        return self._get_attribute(self._SDM_ATT_MAP['ConnectionType'])

    @property
    def DataPathId(self):
        """
        Returns
        -------
        - str: This describes the Data Path ID of the OpenFlow switch.
        """
        return self._get_attribute(self._SDM_ATT_MAP['DataPathId'])

    @property
    def DataPathIdAsHex(self):
        """
        Returns
        -------
        - str: This describes the Data Path ID of the OpenFlow switch in hexadecimal format.
        """
        return self._get_attribute(self._SDM_ATT_MAP['DataPathIdAsHex'])

    @property
    def LocalIp(self):
        """
        Returns
        -------
        - str: This describes the local IP address of the selected interface.
        """
        return self._get_attribute(self._SDM_ATT_MAP['LocalIp'])

    @property
    def LocalPort(self):
        """
        Returns
        -------
        - number: This describes the local port number identifier.
        """
        return self._get_attribute(self._SDM_ATT_MAP['LocalPort'])

    @property
    def RemoteIp(self):
        """
        Returns
        -------
        - str: This describes the Remote IP address of the selected interface.
        """
        return self._get_attribute(self._SDM_ATT_MAP['RemoteIp'])

    @property
    def RemotePort(self):
        """
        Returns
        -------
        - number: This describes the remote port number identifier.
        """
        return self._get_attribute(self._SDM_ATT_MAP['RemotePort'])

    def find(self, AuxiliaryId=None, ConnectionType=None, DataPathId=None, DataPathIdAsHex=None, LocalIp=None, LocalPort=None, RemoteIp=None, RemotePort=None):
        """Finds and retrieves switchAuxiliaryConnectionLearnedInfo resources from the server.

        All named parameters are evaluated on the server using regex. The named parameters can be used to selectively retrieve switchAuxiliaryConnectionLearnedInfo resources from the server.
        To retrieve an exact match ensure the parameter value starts with ^ and ends with $
        By default the find method takes no parameters and will retrieve all switchAuxiliaryConnectionLearnedInfo resources from the server.

        Args
        ----
        - AuxiliaryId (number): This describes the identifier for auxiliary connections.
        - ConnectionType (str(tcp | tls | udp)): This describes the type of OpenFlow connection.
        - DataPathId (str): This describes the Data Path ID of the OpenFlow switch.
        - DataPathIdAsHex (str): This describes the Data Path ID of the OpenFlow switch in hexadecimal format.
        - LocalIp (str): This describes the local IP address of the selected interface.
        - LocalPort (number): This describes the local port number identifier.
        - RemoteIp (str): This describes the Remote IP address of the selected interface.
        - RemotePort (number): This describes the remote port number identifier.

        Returns
        -------
        - self: This instance with matching switchAuxiliaryConnectionLearnedInfo resources retrieved from the server available through an iterator or index

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(self._map_locals(self._SDM_ATT_MAP, locals()))

    def read(self, href):
        """Retrieves a single instance of switchAuxiliaryConnectionLearnedInfo data from the server.

        Args
        ----
        - href (str): An href to the instance to be retrieved

        Returns
        -------
        - self: This instance with the switchAuxiliaryConnectionLearnedInfo resources from the server available through an iterator or index

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)

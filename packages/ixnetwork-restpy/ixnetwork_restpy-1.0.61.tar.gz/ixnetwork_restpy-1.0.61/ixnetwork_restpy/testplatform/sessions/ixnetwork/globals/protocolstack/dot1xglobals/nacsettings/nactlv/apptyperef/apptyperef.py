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


class AppTypeRef(Base):
    """TLV Application Type
    The AppTypeRef class encapsulates a required appTypeRef resource which will be retrieved from the server every time the property is accessed.
    """

    __slots__ = ()
    _SDM_NAME = 'appTypeRef'
    _SDM_ATT_MAP = {
        'Name': 'name',
        'ObjectId': 'objectId',
        'Value': 'value',
    }

    def __init__(self, parent):
        super(AppTypeRef, self).__init__(parent)

    @property
    def NacApps(self):
        """
        Returns
        -------
        - obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.protocolstack.dot1xglobals.nacsettings.nactlv.vendorref.nactypes.nacapps.nacapps.NacApps): An instance of the NacApps class

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.protocolstack.dot1xglobals.nacsettings.nactlv.vendorref.nactypes.nacapps.nacapps import NacApps
        return NacApps(self)

    @property
    def Name(self):
        """
        Returns
        -------
        - str: AppType Name.
        """
        return self._get_attribute(self._SDM_ATT_MAP['Name'])
    @Name.setter
    def Name(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Name'], value)

    @property
    def ObjectId(self):
        """
        Returns
        -------
        - str: Unique identifier for this object
        """
        return self._get_attribute(self._SDM_ATT_MAP['ObjectId'])

    @property
    def Value(self):
        """
        Returns
        -------
        - number: AppType ID.
        """
        return self._get_attribute(self._SDM_ATT_MAP['Value'])
    @Value.setter
    def Value(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Value'], value)

    def update(self, Name=None, Value=None):
        """Updates appTypeRef resource on the server.

        Args
        ----
        - Name (str): AppType Name.
        - Value (number): AppType ID.

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._update(self._map_locals(self._SDM_ATT_MAP, locals()))

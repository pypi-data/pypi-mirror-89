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


class Opaque(Base):
    """
    The Opaque class encapsulates a list of opaque resources that are managed by the system.
    A list of resources can be retrieved from the server using the Opaque.find() method.
    """

    __slots__ = ()
    _SDM_NAME = 'opaque'
    _SDM_ATT_MAP = {
        'EnableRouterTlv': 'enableRouterTlv',
    }

    def __init__(self, parent):
        super(Opaque, self).__init__(parent)

    @property
    def LinkTlv(self):
        """
        Returns
        -------
        - obj(uhd_restpy.testplatform.sessions.ixnetwork.vport.protocols.linktlv_fb695855361b3a0445dcc6b871454c32.LinkTlv): An instance of the LinkTlv class

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        from uhd_restpy.testplatform.sessions.ixnetwork.vport.protocols.linktlv_fb695855361b3a0445dcc6b871454c32 import LinkTlv
        return LinkTlv(self)

    @property
    def RouterTlv(self):
        """
        Returns
        -------
        - obj(uhd_restpy.testplatform.sessions.ixnetwork.vport.protocols.routertlv_c79f980b90b1fb4a01c23bb66ed1380b.RouterTlv): An instance of the RouterTlv class

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        from uhd_restpy.testplatform.sessions.ixnetwork.vport.protocols.routertlv_c79f980b90b1fb4a01c23bb66ed1380b import RouterTlv
        return RouterTlv(self)

    @property
    def EnableRouterTlv(self):
        """
        Returns
        -------
        - bool: 
        """
        return self._get_attribute(self._SDM_ATT_MAP['EnableRouterTlv'])
    @EnableRouterTlv.setter
    def EnableRouterTlv(self, value):
        self._set_attribute(self._SDM_ATT_MAP['EnableRouterTlv'], value)

    def update(self, EnableRouterTlv=None):
        """Updates opaque resource on the server.

        Args
        ----
        - EnableRouterTlv (bool): 

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._update(self._map_locals(self._SDM_ATT_MAP, locals()))

    def find(self, EnableRouterTlv=None):
        """Finds and retrieves opaque resources from the server.

        All named parameters are evaluated on the server using regex. The named parameters can be used to selectively retrieve opaque resources from the server.
        To retrieve an exact match ensure the parameter value starts with ^ and ends with $
        By default the find method takes no parameters and will retrieve all opaque resources from the server.

        Args
        ----
        - EnableRouterTlv (bool): 

        Returns
        -------
        - self: This instance with matching opaque resources retrieved from the server available through an iterator or index

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(self._map_locals(self._SDM_ATT_MAP, locals()))

    def read(self, href):
        """Retrieves a single instance of opaque data from the server.

        Args
        ----
        - href (str): An href to the instance to be retrieved

        Returns
        -------
        - self: This instance with the opaque resources from the server available through an iterator or index

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)

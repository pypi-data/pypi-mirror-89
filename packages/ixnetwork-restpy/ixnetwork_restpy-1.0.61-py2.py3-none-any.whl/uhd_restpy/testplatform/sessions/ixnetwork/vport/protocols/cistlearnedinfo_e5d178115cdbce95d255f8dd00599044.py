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


class CistLearnedInfo(Base):
    """Learned information associated with a CIST on an (MSTP) stpBridge.
    The CistLearnedInfo class encapsulates a required cistLearnedInfo resource which will be retrieved from the server every time the property is accessed.
    """

    __slots__ = ()
    _SDM_NAME = 'cistLearnedInfo'
    _SDM_ATT_MAP = {
        'RegRootCost': 'regRootCost',
        'RegRootMac': 'regRootMac',
        'RegRootPriority': 'regRootPriority',
        'RootCost': 'rootCost',
        'RootMac': 'rootMac',
        'RootPriority': 'rootPriority',
    }

    def __init__(self, parent):
        super(CistLearnedInfo, self).__init__(parent)

    @property
    def RegRootCost(self):
        """
        Returns
        -------
        - number: (Read-only) The cost for the shortest path from the advertising bridge to the regional root bridge.
        """
        return self._get_attribute(self._SDM_ATT_MAP['RegRootCost'])

    @property
    def RegRootMac(self):
        """
        Returns
        -------
        - str: (Read-only) The regional root MAC address being advertised by the bridge.
        """
        return self._get_attribute(self._SDM_ATT_MAP['RegRootMac'])

    @property
    def RegRootPriority(self):
        """
        Returns
        -------
        - number: (Read-only) The regional root priority being advertised by the bridge.
        """
        return self._get_attribute(self._SDM_ATT_MAP['RegRootPriority'])

    @property
    def RootCost(self):
        """
        Returns
        -------
        - number: (Read-only) The cost for the shortest path from the advertising bridge to the root bridge.
        """
        return self._get_attribute(self._SDM_ATT_MAP['RootCost'])

    @property
    def RootMac(self):
        """
        Returns
        -------
        - str: (Read-only) The root bridge MAC address being advertised.
        """
        return self._get_attribute(self._SDM_ATT_MAP['RootMac'])

    @property
    def RootPriority(self):
        """
        Returns
        -------
        - number: (Read-only) The priority being advertised for the root bridge.
        """
        return self._get_attribute(self._SDM_ATT_MAP['RootPriority'])

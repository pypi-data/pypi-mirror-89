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


class MobilePathEntries(Base):
    """
    The MobilePathEntries class encapsulates a list of mobilePathEntries resources that are managed by the user.
    A list of resources can be retrieved from the server using the MobilePathEntries.find() method.
    The list can be managed by using the MobilePathEntries.add() and MobilePathEntries.remove() methods.
    """

    __slots__ = ()
    _SDM_NAME = 'mobilePathEntries'
    _SDM_ATT_MAP = {
        'NextENodeB': 'nextENodeB',
        'NextRange': 'nextRange',
        'ObjectId': 'objectId',
        'RelocateSgw': 'relocateSgw',
    }

    def __init__(self, parent):
        super(MobilePathEntries, self).__init__(parent)

    @property
    def NextENodeB(self):
        """
        Returns
        -------
        - str(None | /api/v1/sessions/1/ixnetwork/vport/.../range): Obsolete. Use nextRange instead.
        """
        return self._get_attribute(self._SDM_ATT_MAP['NextENodeB'])
    @NextENodeB.setter
    def NextENodeB(self, value):
        self._set_attribute(self._SDM_ATT_MAP['NextENodeB'], value)

    @property
    def NextRange(self):
        """
        Returns
        -------
        - str(None | /api/v1/sessions/1/ixnetwork/vport/.../range): 
        """
        return self._get_attribute(self._SDM_ATT_MAP['NextRange'])
    @NextRange.setter
    def NextRange(self, value):
        self._set_attribute(self._SDM_ATT_MAP['NextRange'], value)

    @property
    def ObjectId(self):
        """
        Returns
        -------
        - str: Unique identifier for this object
        """
        return self._get_attribute(self._SDM_ATT_MAP['ObjectId'])

    @property
    def RelocateSgw(self):
        """
        Returns
        -------
        - bool: Perform SGW change on TAU or Handover.
        """
        return self._get_attribute(self._SDM_ATT_MAP['RelocateSgw'])
    @RelocateSgw.setter
    def RelocateSgw(self, value):
        self._set_attribute(self._SDM_ATT_MAP['RelocateSgw'], value)

    def update(self, NextENodeB=None, NextRange=None, RelocateSgw=None):
        """Updates mobilePathEntries resource on the server.

        Args
        ----
        - NextENodeB (str(None | /api/v1/sessions/1/ixnetwork/vport/.../range)): Obsolete. Use nextRange instead.
        - NextRange (str(None | /api/v1/sessions/1/ixnetwork/vport/.../range)): 
        - RelocateSgw (bool): Perform SGW change on TAU or Handover.

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._update(self._map_locals(self._SDM_ATT_MAP, locals()))

    def add(self, NextENodeB=None, NextRange=None, RelocateSgw=None):
        """Adds a new mobilePathEntries resource on the server and adds it to the container.

        Args
        ----
        - NextENodeB (str(None | /api/v1/sessions/1/ixnetwork/vport/.../range)): Obsolete. Use nextRange instead.
        - NextRange (str(None | /api/v1/sessions/1/ixnetwork/vport/.../range)): 
        - RelocateSgw (bool): Perform SGW change on TAU or Handover.

        Returns
        -------
        - self: This instance with all currently retrieved mobilePathEntries resources using find and the newly added mobilePathEntries resources available through an iterator or index

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._create(self._map_locals(self._SDM_ATT_MAP, locals()))

    def remove(self):
        """Deletes all the contained mobilePathEntries resources in this instance from the server.

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        self._delete()

    def find(self, NextENodeB=None, NextRange=None, ObjectId=None, RelocateSgw=None):
        """Finds and retrieves mobilePathEntries resources from the server.

        All named parameters are evaluated on the server using regex. The named parameters can be used to selectively retrieve mobilePathEntries resources from the server.
        To retrieve an exact match ensure the parameter value starts with ^ and ends with $
        By default the find method takes no parameters and will retrieve all mobilePathEntries resources from the server.

        Args
        ----
        - NextENodeB (str(None | /api/v1/sessions/1/ixnetwork/vport/.../range)): Obsolete. Use nextRange instead.
        - NextRange (str(None | /api/v1/sessions/1/ixnetwork/vport/.../range)): 
        - ObjectId (str): Unique identifier for this object
        - RelocateSgw (bool): Perform SGW change on TAU or Handover.

        Returns
        -------
        - self: This instance with matching mobilePathEntries resources retrieved from the server available through an iterator or index

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(self._map_locals(self._SDM_ATT_MAP, locals()))

    def read(self, href):
        """Retrieves a single instance of mobilePathEntries data from the server.

        Args
        ----
        - href (str): An href to the instance to be retrieved

        Returns
        -------
        - self: This instance with the mobilePathEntries resources from the server available through an iterator or index

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)

    def CustomProtocolStack(self, *args, **kwargs):
        """Executes the customProtocolStack operation on the server.

        Create custom protocol stack under /vport/protocolStack

        customProtocolStack(Arg2=list, Arg3=enum)
        -----------------------------------------
        - Arg2 (list(str)): List of plugin types to be added in the new custom stack
        - Arg3 (str(kAppend | kMerge | kOverwrite)): Append, merge or overwrite existing protocol stack

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('customProtocolStack', payload=payload, response_object=None)

    def DisableProtocolStack(self, *args, **kwargs):
        """Executes the disableProtocolStack operation on the server.

        Disable a protocol under protocolStack using the class name

        disableProtocolStack(Arg2=string)string
        ---------------------------------------
        - Arg2 (str): Protocol class name to disable
        - Returns str: Status of the exec

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('disableProtocolStack', payload=payload, response_object=None)

    def EnableProtocolStack(self, *args, **kwargs):
        """Executes the enableProtocolStack operation on the server.

        Enable a protocol under protocolStack using the class name

        enableProtocolStack(Arg2=string)string
        --------------------------------------
        - Arg2 (str): Protocol class name to enable
        - Returns str: Status of the exec

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('enableProtocolStack', payload=payload, response_object=None)

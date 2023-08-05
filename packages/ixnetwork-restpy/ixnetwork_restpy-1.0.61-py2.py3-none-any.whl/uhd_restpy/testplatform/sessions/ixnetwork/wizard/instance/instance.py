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


class Instance(Base):
    """
    The Instance class encapsulates a list of instance resources that are managed by the user.
    A list of resources can be retrieved from the server using the Instance.find() method.
    The list can be managed by using the Instance.add() and Instance.remove() methods.
    """

    __slots__ = ()
    _SDM_NAME = 'instance'
    _SDM_ATT_MAP = {
        'LastUpdate': 'lastUpdate',
        'ScriptCompleteTime': 'scriptCompleteTime',
        'ScriptResult': 'scriptResult',
        'TemplateRef': 'templateRef',
    }

    def __init__(self, parent):
        super(Instance, self).__init__(parent)

    @property
    def Render(self):
        """
        Returns
        -------
        - obj(uhd_restpy.testplatform.sessions.ixnetwork.wizard.instance.render.render.Render): An instance of the Render class

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        from uhd_restpy.testplatform.sessions.ixnetwork.wizard.instance.render.render import Render
        return Render(self)._select()

    @property
    def Step(self):
        """
        Returns
        -------
        - obj(uhd_restpy.testplatform.sessions.ixnetwork.wizard.instance.step.step.Step): An instance of the Step class

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        from uhd_restpy.testplatform.sessions.ixnetwork.wizard.instance.step.step import Step
        return Step(self)

    @property
    def LastUpdate(self):
        """
        Returns
        -------
        - str: timestamp of the last update which requires client side refresh
        """
        return self._get_attribute(self._SDM_ATT_MAP['LastUpdate'])
    @LastUpdate.setter
    def LastUpdate(self, value):
        self._set_attribute(self._SDM_ATT_MAP['LastUpdate'], value)

    @property
    def ScriptCompleteTime(self):
        """
        Returns
        -------
        - str: time last script run completed
        """
        return self._get_attribute(self._SDM_ATT_MAP['ScriptCompleteTime'])

    @property
    def ScriptResult(self):
        """
        Returns
        -------
        - str: result from last wizard run
        """
        return self._get_attribute(self._SDM_ATT_MAP['ScriptResult'])

    @property
    def TemplateRef(self):
        """
        Returns
        -------
        - str(None | /api/v1/sessions/1/ixnetwork/wizard/.../*): wizard template used to create this instance
        """
        return self._get_attribute(self._SDM_ATT_MAP['TemplateRef'])
    @TemplateRef.setter
    def TemplateRef(self, value):
        self._set_attribute(self._SDM_ATT_MAP['TemplateRef'], value)

    def update(self, LastUpdate=None, TemplateRef=None):
        """Updates instance resource on the server.

        Args
        ----
        - LastUpdate (str): timestamp of the last update which requires client side refresh
        - TemplateRef (str(None | /api/v1/sessions/1/ixnetwork/wizard/.../*)): wizard template used to create this instance

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._update(self._map_locals(self._SDM_ATT_MAP, locals()))

    def add(self, LastUpdate=None, TemplateRef=None):
        """Adds a new instance resource on the server and adds it to the container.

        Args
        ----
        - LastUpdate (str): timestamp of the last update which requires client side refresh
        - TemplateRef (str(None | /api/v1/sessions/1/ixnetwork/wizard/.../*)): wizard template used to create this instance

        Returns
        -------
        - self: This instance with all currently retrieved instance resources using find and the newly added instance resources available through an iterator or index

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._create(self._map_locals(self._SDM_ATT_MAP, locals()))

    def remove(self):
        """Deletes all the contained instance resources in this instance from the server.

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        self._delete()

    def find(self, LastUpdate=None, ScriptCompleteTime=None, ScriptResult=None, TemplateRef=None):
        """Finds and retrieves instance resources from the server.

        All named parameters are evaluated on the server using regex. The named parameters can be used to selectively retrieve instance resources from the server.
        To retrieve an exact match ensure the parameter value starts with ^ and ends with $
        By default the find method takes no parameters and will retrieve all instance resources from the server.

        Args
        ----
        - LastUpdate (str): timestamp of the last update which requires client side refresh
        - ScriptCompleteTime (str): time last script run completed
        - ScriptResult (str): result from last wizard run
        - TemplateRef (str(None | /api/v1/sessions/1/ixnetwork/wizard/.../*)): wizard template used to create this instance

        Returns
        -------
        - self: This instance with matching instance resources retrieved from the server available through an iterator or index

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(self._map_locals(self._SDM_ATT_MAP, locals()))

    def read(self, href):
        """Retrieves a single instance of instance data from the server.

        Args
        ----
        - href (str): An href to the instance to be retrieved

        Returns
        -------
        - self: This instance with the instance resources from the server available through an iterator or index

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)

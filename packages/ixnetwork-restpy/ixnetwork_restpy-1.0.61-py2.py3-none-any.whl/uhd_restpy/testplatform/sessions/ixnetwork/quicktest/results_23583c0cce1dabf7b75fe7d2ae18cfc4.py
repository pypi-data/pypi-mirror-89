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


class Results(Base):
    """This object shows the results of the DHCP server in progress.
    The Results class encapsulates a required results resource which will be retrieved from the server every time the property is accessed.
    """

    __slots__ = ()
    _SDM_NAME = 'results'
    _SDM_ATT_MAP = {
        'CurrentActions': 'currentActions',
        'CurrentViews': 'currentViews',
        'Duration': 'duration',
        'IsRunning': 'isRunning',
        'Progress': 'progress',
        'Result': 'result',
        'ResultPath': 'resultPath',
        'StartTime': 'startTime',
        'Status': 'status',
        'TrafficStatus': 'trafficStatus',
        'WaitingStatus': 'waitingStatus',
    }

    def __init__(self, parent):
        super(Results, self).__init__(parent)

    @property
    def CurrentActions(self):
        """
        Returns
        -------
        - list(dict(arg1:str,arg2:str[AgingTable | ApplyFlowGroups | CheckingForAvailableStats | CheckingLicense | ClearingStats | CollectingStats | DropLink | frameLossCriteriaNotMet | HoldDown | InitializingTest | IterationStart | LicenseFailed | LicenseVerified | None | NoRibInConvergenceStopping | ReleasingResources | SendingLearningFrames | SetTestConfiguration | SetupStatisticsCollection | StartingTraffic | TestEnded | TestStarted | ThresholdReachedStopping | TransmittingComplete | TransmittingFrames | WaitAfterFailover | WaitBeforeFailover | WaitingAfterLearningFramesSent | WaitingBeforeSendingTraffic | WaitingForDelayBetweenIterations | WaitingForPorts | WaitingForStats | WaitingTrafficToStop])): Current actions
        """
        return self._get_attribute(self._SDM_ATT_MAP['CurrentActions'])

    @property
    def CurrentViews(self):
        """
        Returns
        -------
        - list(str): Views used by this QuickTest
        """
        return self._get_attribute(self._SDM_ATT_MAP['CurrentViews'])

    @property
    def Duration(self):
        """
        Returns
        -------
        - str: Test duration
        """
        return self._get_attribute(self._SDM_ATT_MAP['Duration'])

    @property
    def IsRunning(self):
        """
        Returns
        -------
        - bool: Indicates whether the test is currently running
        """
        return self._get_attribute(self._SDM_ATT_MAP['IsRunning'])

    @property
    def Progress(self):
        """
        Returns
        -------
        - str: Test progress
        """
        return self._get_attribute(self._SDM_ATT_MAP['Progress'])

    @property
    def Result(self):
        """
        Returns
        -------
        - str: Test result
        """
        return self._get_attribute(self._SDM_ATT_MAP['Result'])

    @property
    def ResultPath(self):
        """
        Returns
        -------
        - str: Folder containing test result files
        """
        return self._get_attribute(self._SDM_ATT_MAP['ResultPath'])

    @property
    def StartTime(self):
        """
        Returns
        -------
        - str: Test start time
        """
        return self._get_attribute(self._SDM_ATT_MAP['StartTime'])

    @property
    def Status(self):
        """
        Returns
        -------
        - str: Test status
        """
        return self._get_attribute(self._SDM_ATT_MAP['Status'])

    @property
    def TrafficStatus(self):
        """
        Returns
        -------
        - dict(arg1:number,arg2:number): Test traffic status
        """
        return self._get_attribute(self._SDM_ATT_MAP['TrafficStatus'])

    @property
    def WaitingStatus(self):
        """
        Returns
        -------
        - dict(arg1:number,arg2:number): Test waiting status
        """
        return self._get_attribute(self._SDM_ATT_MAP['WaitingStatus'])

    def Apply(self):
        """Executes the apply operation on the server.

        Applies the specified Quick Test.

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        return self._execute('apply', payload=payload, response_object=None)

    def ApplyAsync(self):
        """Executes the applyAsync operation on the server.

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        return self._execute('applyAsync', payload=payload, response_object=None)

    def ApplyAsyncResult(self):
        """Executes the applyAsyncResult operation on the server.

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        return self._execute('applyAsyncResult', payload=payload, response_object=None)

    def ApplyITWizardConfiguration(self):
        """Executes the applyITWizardConfiguration operation on the server.

        Applies the specified Quick Test.

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        return self._execute('applyITWizardConfiguration', payload=payload, response_object=None)

    def GenerateReport(self):
        """Executes the generateReport operation on the server.

        Generate a PDF report for the last succesfull test run.

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        return self._execute('generateReport', payload=payload, response_object=None)

    def Run(self, *args, **kwargs):
        """Executes the run operation on the server.

        Starts the specified Quick Test and waits for its execution to finish.

        The IxNetwork model allows for multiple method Signatures with the same name while python does not.

        run(InputParameters=string)list
        -------------------------------
        - InputParameters (str): The input arguments of the test.
        - Returns list(str): This method is synchronous and returns the result of the test.

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('run', payload=payload, response_object=None)

    def Start(self, *args, **kwargs):
        """Executes the start operation on the server.

        Starts the specified Quick Test.

        The IxNetwork model allows for multiple method Signatures with the same name while python does not.

        start(InputParameters=string)
        -----------------------------
        - InputParameters (str): The input arguments of the test.

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('start', payload=payload, response_object=None)

    def Stop(self):
        """Executes the stop operation on the server.

        Stops the currently running Quick Test.

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        return self._execute('stop', payload=payload, response_object=None)

    def WaitForTest(self):
        """Executes the waitForTest operation on the server.

        Waits for the execution of the specified Quick Test to be completed.

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        return self._execute('waitForTest', payload=payload, response_object=None)

from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Average:
	"""Average commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("average", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:LTE:SIGNaling<instance>:THRoughput:TRACe:UL:PDU:AVERage \n
		Snippet: value: List[float] = driver.throughput.trace.uplink.pdu.average.fetch() \n
		Returns the values of the uplink throughput traces. The results of the current and average traces can be retrieved. The
		number of trace values n depends on the configured update interval and window size: n = integer (<window size> / <update
		interval>) + 1 \n
		Use RsCmwLteSig.reliability.last_value to read the updated reliability indicator. \n
			:return: uplink_pdu: Comma-separated list of n throughput values Unit: bit/s"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:LTE:SIGNaling<Instance>:THRoughput:TRACe:UL:PDU:AVERage?', suppressed)
		return response

	def read(self) -> List[float]:
		"""SCPI: READ:LTE:SIGNaling<instance>:THRoughput:TRACe:UL:PDU:AVERage \n
		Snippet: value: List[float] = driver.throughput.trace.uplink.pdu.average.read() \n
		Returns the values of the uplink throughput traces. The results of the current and average traces can be retrieved. The
		number of trace values n depends on the configured update interval and window size: n = integer (<window size> / <update
		interval>) + 1 \n
		Use RsCmwLteSig.reliability.last_value to read the updated reliability indicator. \n
			:return: uplink_pdu: Comma-separated list of n throughput values Unit: bit/s"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:LTE:SIGNaling<Instance>:THRoughput:TRACe:UL:PDU:AVERage?', suppressed)
		return response

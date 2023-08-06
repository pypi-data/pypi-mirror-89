from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Relative:
	"""Relative commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("relative", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: See 'Reliability Indicator'
			- Sent: List[float]: NAV returned, for future use
			- Ack: List[float]: Received acknowledgments (percentage of ACK+NACK+DTX in the column) Range: 0 % to 100 %, Unit: %
			- Nack: List[float]: Received negative acknowledgments (percentage of ACK+NACK+DTX in the column) Range: 0 % to 100 %, Unit: %
			- Dtx: List[float]: Sent subframes for which no ACK and no NACK has been received (percentage of ACK+NACK+DTX in the column) Range: 0 % to 100 %, Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct('Sent', DataType.FloatList, None, False, True, 1),
			ArgStruct('Ack', DataType.FloatList, None, False, True, 1),
			ArgStruct('Nack', DataType.FloatList, None, False, True, 1),
			ArgStruct('Dtx', DataType.FloatList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Sent: List[float] = None
			self.Ack: List[float] = None
			self.Nack: List[float] = None
			self.Dtx: List[float] = None

	def fetch(self, secondaryCompCarrier=repcap.SecondaryCompCarrier.Default, stream=repcap.Stream.Default) -> FetchStruct:
		"""SCPI: FETCh:LTE:SIGNaling<instance>:EBLer:SCC<Carrier>:HARQ:STReam<Stream>:SUBFrame:RELative \n
		Snippet: value: FetchStruct = driver.extendedBler.scc.harq.stream.subframe.relative.fetch(secondaryCompCarrier = repcap.SecondaryCompCarrier.Default, stream = repcap.Stream.Default) \n
		Returns relative HARQ results for one downlink stream. All columns of the 'HARQ per Subframe' result table are returned:
		<Reliability>, {<Sent>, <ACK>, <NACK>, <DTX>}column 0, {...}column 1, ..., {...}column 9 \n
			:param secondaryCompCarrier: optional repeated capability selector. Default value: CC1 (settable in the interface 'Scc')
			:param stream: optional repeated capability selector. Default value: S1 (settable in the interface 'Stream')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		secondaryCompCarrier_cmd_val = self._base.get_repcap_cmd_value(secondaryCompCarrier, repcap.SecondaryCompCarrier)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		return self._core.io.query_struct(f'FETCh:LTE:SIGNaling<Instance>:EBLer:SCC{secondaryCompCarrier_cmd_val}:HARQ:STReam{stream_cmd_val}:SUBFrame:RELative?', self.__class__.FetchStruct())

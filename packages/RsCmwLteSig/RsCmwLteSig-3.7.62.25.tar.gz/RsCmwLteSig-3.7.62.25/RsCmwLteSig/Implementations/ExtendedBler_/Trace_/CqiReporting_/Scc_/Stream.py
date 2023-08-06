from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Stream:
	"""Stream commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: Stream, default value after init: Stream.S1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("stream", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_stream_get', 'repcap_stream_set', repcap.Stream.S1)

	def repcap_stream_set(self, enum_value: repcap.Stream) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Stream.Default
		Default value after init: Stream.S1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_stream_get(self) -> repcap.Stream:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def fetch(self, secondaryCompCarrier=repcap.SecondaryCompCarrier.Default, stream=repcap.Stream.Default) -> List[float]:
		"""SCPI: FETCh:LTE:SIGNaling<instance>:EBLer:TRACe:CQIReporting:SCC<Carrier>:STReam<Stream> \n
		Snippet: value: List[float] = driver.extendedBler.trace.cqiReporting.scc.stream.fetch(secondaryCompCarrier = repcap.SecondaryCompCarrier.Default, stream = repcap.Stream.Default) \n
		Returns the Y-values of the CQI index bar graph for one downlink stream. \n
		Use RsCmwLteSig.reliability.last_value to read the updated reliability indicator. \n
			:param secondaryCompCarrier: optional repeated capability selector. Default value: CC1 (settable in the interface 'Scc')
			:param stream: optional repeated capability selector. Default value: S1 (settable in the interface 'Stream')
			:return: yvalue: Comma-separated list of 16 Y-values, for CQI index 0 to 15 Range: 0 to 2E+9"""
		secondaryCompCarrier_cmd_val = self._base.get_repcap_cmd_value(secondaryCompCarrier, repcap.SecondaryCompCarrier)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:LTE:SIGNaling<Instance>:EBLer:TRACe:CQIReporting:SCC{secondaryCompCarrier_cmd_val}:STReam{stream_cmd_val}?', suppressed)
		return response

	def clone(self) -> 'Stream':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Stream(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

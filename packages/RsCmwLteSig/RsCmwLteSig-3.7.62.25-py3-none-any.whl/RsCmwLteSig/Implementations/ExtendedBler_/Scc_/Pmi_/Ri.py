from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ri:
	"""Ri commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: ReliabilityIndicatorNo, default value after init: ReliabilityIndicatorNo.RIno1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ri", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_reliabilityIndicatorNo_get', 'repcap_reliabilityIndicatorNo_set', repcap.ReliabilityIndicatorNo.RIno1)

	def repcap_reliabilityIndicatorNo_set(self, enum_value: repcap.ReliabilityIndicatorNo) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to ReliabilityIndicatorNo.Default
		Default value after init: ReliabilityIndicatorNo.RIno1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_reliabilityIndicatorNo_get(self) -> repcap.ReliabilityIndicatorNo:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def fetch(self, secondaryCompCarrier=repcap.SecondaryCompCarrier.Default, reliabilityIndicatorNo=repcap.ReliabilityIndicatorNo.Default) -> List[int]:
		"""SCPI: FETCh:LTE:SIGNaling<instance>:EBLer:SCC<Carrier>:PMI:RI<no> \n
		Snippet: value: List[int] = driver.extendedBler.scc.pmi.ri.fetch(secondaryCompCarrier = repcap.SecondaryCompCarrier.Default, reliabilityIndicatorNo = repcap.ReliabilityIndicatorNo.Default) \n
		Returns the PMI results for the RI value <no>. \n
		Use RsCmwLteSig.reliability.last_value to read the updated reliability indicator. \n
			:param secondaryCompCarrier: optional repeated capability selector. Default value: CC1 (settable in the interface 'Scc')
			:param reliabilityIndicatorNo: optional repeated capability selector. Default value: RIno1 (settable in the interface 'Ri')
			:return: pmi: Comma-separated list of values, indicating the number of received PMI values, see table Range: 0 to 2E+9"""
		secondaryCompCarrier_cmd_val = self._base.get_repcap_cmd_value(secondaryCompCarrier, repcap.SecondaryCompCarrier)
		reliabilityIndicatorNo_cmd_val = self._base.get_repcap_cmd_value(reliabilityIndicatorNo, repcap.ReliabilityIndicatorNo)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_int_list_suppressed(f'FETCh:LTE:SIGNaling<Instance>:EBLer:SCC{secondaryCompCarrier_cmd_val}:PMI:RI{reliabilityIndicatorNo_cmd_val}?', suppressed)
		return response

	def clone(self) -> 'Ri':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ri(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

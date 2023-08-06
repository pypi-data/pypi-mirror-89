from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Csamples:
	"""Csamples commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: ClippingCounter, default value after init: ClippingCounter.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("csamples", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_clippingCounter_get', 'repcap_clippingCounter_set', repcap.ClippingCounter.Nr1)

	def repcap_clippingCounter_set(self, enum_value: repcap.ClippingCounter) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to ClippingCounter.Default
		Default value after init: ClippingCounter.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_clippingCounter_get(self) -> repcap.ClippingCounter:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def get(self, secondaryCompCarrier=repcap.SecondaryCompCarrier.Default, clippingCounter=repcap.ClippingCounter.Default) -> float:
		"""SCPI: SENSe:LTE:SIGNaling<instance>:FADing:SCC<Carrier>:FSIMulator:ILOSs:CSAMples<ClippingCounter> \n
		Snippet: value: float = driver.sense.fading.scc.fadingSimulator.insertionLoss.csamples.get(secondaryCompCarrier = repcap.SecondaryCompCarrier.Default, clippingCounter = repcap.ClippingCounter.Default) \n
		Returns the percentage of clipped samples for the output path number <n>. \n
			:param secondaryCompCarrier: optional repeated capability selector. Default value: CC1 (settable in the interface 'Scc')
			:param clippingCounter: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Csamples')
			:return: clipped_samples: Range: 0 % to 100 %, Unit: %"""
		secondaryCompCarrier_cmd_val = self._base.get_repcap_cmd_value(secondaryCompCarrier, repcap.SecondaryCompCarrier)
		clippingCounter_cmd_val = self._base.get_repcap_cmd_value(clippingCounter, repcap.ClippingCounter)
		response = self._core.io.query_str(f'SENSe:LTE:SIGNaling<Instance>:FADing:SCC{secondaryCompCarrier_cmd_val}:FSIMulator:ILOSs:CSAMples{clippingCounter_cmd_val}?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'Csamples':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Csamples(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

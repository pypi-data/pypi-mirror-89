from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Enable:
	"""Enable commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("enable", core, parent)

	@property
	def mimo(self):
		"""mimo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mimo'):
			from .Enable_.Mimo import Mimo
			self._mimo = Mimo(self._core, self._base)
		return self._mimo

	def set(self, enable: bool, secondaryCompCarrier=repcap.SecondaryCompCarrier.Default) -> None:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:CONNection:SCC<Carrier>:SCHModel:ENABle \n
		Snippet: driver.configure.connection.scc.schModel.enable.set(enable = False, secondaryCompCarrier = repcap.SecondaryCompCarrier.Default) \n
		Enables or disables the MIMO 2x2 static channel matrix. Disabling the channel matrix results in an ideal radio channel
		without any coupling between the downlink signals. \n
			:param enable: OFF | ON
			:param secondaryCompCarrier: optional repeated capability selector. Default value: CC1 (settable in the interface 'Scc')"""
		param = Conversions.bool_to_str(enable)
		secondaryCompCarrier_cmd_val = self._base.get_repcap_cmd_value(secondaryCompCarrier, repcap.SecondaryCompCarrier)
		self._core.io.write(f'CONFigure:LTE:SIGNaling<Instance>:CONNection:SCC{secondaryCompCarrier_cmd_val}:SCHModel:ENABle {param}')

	def get(self, secondaryCompCarrier=repcap.SecondaryCompCarrier.Default) -> bool:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:CONNection:SCC<Carrier>:SCHModel:ENABle \n
		Snippet: value: bool = driver.configure.connection.scc.schModel.enable.get(secondaryCompCarrier = repcap.SecondaryCompCarrier.Default) \n
		Enables or disables the MIMO 2x2 static channel matrix. Disabling the channel matrix results in an ideal radio channel
		without any coupling between the downlink signals. \n
			:param secondaryCompCarrier: optional repeated capability selector. Default value: CC1 (settable in the interface 'Scc')
			:return: enable: OFF | ON"""
		secondaryCompCarrier_cmd_val = self._base.get_repcap_cmd_value(secondaryCompCarrier, repcap.SecondaryCompCarrier)
		response = self._core.io.query_str(f'CONFigure:LTE:SIGNaling<Instance>:CONNection:SCC{secondaryCompCarrier_cmd_val}:SCHModel:ENABle?')
		return Conversions.str_to_bool(response)

	def clone(self) -> 'Enable':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Enable(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

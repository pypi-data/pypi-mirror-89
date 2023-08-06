from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tia:
	"""Tia commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: TbsIndexAlt, default value after init: TbsIndexAlt.Nr2"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tia", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_tbsIndexAlt_get', 'repcap_tbsIndexAlt_set', repcap.TbsIndexAlt.Nr2)

	def repcap_tbsIndexAlt_set(self, enum_value: repcap.TbsIndexAlt) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to TbsIndexAlt.Default
		Default value after init: TbsIndexAlt.Nr2"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_tbsIndexAlt_get(self) -> repcap.TbsIndexAlt:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def set(self, enable: bool, tbsIndexAlt=repcap.TbsIndexAlt.Default) -> None:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:CONNection[:PCC]:TIA<Nr> \n
		Snippet: driver.configure.connection.pcc.tia.set(enable = False, tbsIndexAlt = repcap.TbsIndexAlt.Default) \n
		Enables or disables sending the parameter 'tbsIndexAlt2-r14' to the UE. \n
			:param enable: OFF | ON
			:param tbsIndexAlt: optional repeated capability selector. Default value: Nr2 (settable in the interface 'Tia')"""
		param = Conversions.bool_to_str(enable)
		tbsIndexAlt_cmd_val = self._base.get_repcap_cmd_value(tbsIndexAlt, repcap.TbsIndexAlt)
		self._core.io.write(f'CONFigure:LTE:SIGNaling<Instance>:CONNection:PCC:TIA{tbsIndexAlt_cmd_val} {param}')

	def get(self, tbsIndexAlt=repcap.TbsIndexAlt.Default) -> bool:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:CONNection[:PCC]:TIA<Nr> \n
		Snippet: value: bool = driver.configure.connection.pcc.tia.get(tbsIndexAlt = repcap.TbsIndexAlt.Default) \n
		Enables or disables sending the parameter 'tbsIndexAlt2-r14' to the UE. \n
			:param tbsIndexAlt: optional repeated capability selector. Default value: Nr2 (settable in the interface 'Tia')
			:return: enable: OFF | ON"""
		tbsIndexAlt_cmd_val = self._base.get_repcap_cmd_value(tbsIndexAlt, repcap.TbsIndexAlt)
		response = self._core.io.query_str(f'CONFigure:LTE:SIGNaling<Instance>:CONNection:PCC:TIA{tbsIndexAlt_cmd_val}?')
		return Conversions.str_to_bool(response)

	def clone(self) -> 'Tia':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tia(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

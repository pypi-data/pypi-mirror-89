from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Eattenuation:
	"""Eattenuation commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("eattenuation", core, parent)

	@property
	def output(self):
		"""output commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_output'):
			from .Eattenuation_.Output import Output
			self._output = Output(self._core, self._base)
		return self._output

	def get_input_py(self) -> float:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:RFSettings[:PCC]:EATTenuation:INPut \n
		Snippet: value: float = driver.configure.rfSettings.pcc.eattenuation.get_input_py() \n
		Defines an external attenuation (or gain, if the value is negative) , to be applied to the RF input connector. \n
			:return: ext_rf_in_att: Range: -50 dB to 90 dB, Unit: dB
		"""
		response = self._core.io.query_str('CONFigure:LTE:SIGNaling<Instance>:RFSettings:PCC:EATTenuation:INPut?')
		return Conversions.str_to_float(response)

	def set_input_py(self, ext_rf_in_att: float) -> None:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:RFSettings[:PCC]:EATTenuation:INPut \n
		Snippet: driver.configure.rfSettings.pcc.eattenuation.set_input_py(ext_rf_in_att = 1.0) \n
		Defines an external attenuation (or gain, if the value is negative) , to be applied to the RF input connector. \n
			:param ext_rf_in_att: Range: -50 dB to 90 dB, Unit: dB
		"""
		param = Conversions.decimal_value_to_str(ext_rf_in_att)
		self._core.io.write(f'CONFigure:LTE:SIGNaling<Instance>:RFSettings:PCC:EATTenuation:INPut {param}')

	def clone(self) -> 'Eattenuation':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Eattenuation(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

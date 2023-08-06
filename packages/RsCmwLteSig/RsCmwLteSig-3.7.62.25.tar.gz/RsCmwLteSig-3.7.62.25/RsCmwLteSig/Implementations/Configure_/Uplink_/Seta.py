from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Seta:
	"""Seta commands group definition. 17 total commands, 3 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("seta", core, parent)

	@property
	def pusch(self):
		"""pusch commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_pusch'):
			from .Seta_.Pusch import Pusch
			self._pusch = Pusch(self._core, self._base)
		return self._pusch

	@property
	def apPower(self):
		"""apPower commands group. 5 Sub-classes, 1 commands."""
		if not hasattr(self, '_apPower'):
			from .Seta_.ApPower import ApPower
			self._apPower = ApPower(self._core, self._base)
		return self._apPower

	@property
	def pucch(self):
		"""pucch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pucch'):
			from .Seta_.Pucch import Pucch
			self._pucch = Pucch(self._core, self._base)
		return self._pucch

	def get_power_max(self) -> float or bool:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:UL:SETA:PMAX \n
		Snippet: value: float or bool = driver.configure.uplink.seta.get_power_max() \n
		Specifies the maximum allowed UE power. \n
			:return: power: Range: -30 dBm to 33 dBm, Unit: dBm Additional parameters: OFF | ON (disables | enables signaling of the value to the UE)
		"""
		response = self._core.io.query_str('CONFigure:LTE:SIGNaling<Instance>:UL:SETA:PMAX?')
		return Conversions.str_to_float_or_bool(response)

	def set_power_max(self, power: float or bool) -> None:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:UL:SETA:PMAX \n
		Snippet: driver.configure.uplink.seta.set_power_max(power = 1.0) \n
		Specifies the maximum allowed UE power. \n
			:param power: Range: -30 dBm to 33 dBm, Unit: dBm Additional parameters: OFF | ON (disables | enables signaling of the value to the UE)
		"""
		param = Conversions.decimal_or_bool_value_to_str(power)
		self._core.io.write(f'CONFigure:LTE:SIGNaling<Instance>:UL:SETA:PMAX {param}')

	def clone(self) -> 'Seta':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Seta(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

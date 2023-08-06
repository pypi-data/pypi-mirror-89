from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CltPower:
	"""CltPower commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cltPower", core, parent)

	def get_offset(self) -> float:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:UL:SETB:PUSCh:TPC:CLTPower:OFFSet \n
		Snippet: value: float = driver.configure.uplink.setb.pusch.tpc.cltPower.get_offset() \n
		Defines a target power offset relative to the power master CC, for power control with the TPC setup CLOop. The setting is
		irrelevant for carriers with independent UL power control. \n
			:return: offset: Target power = master target power + Offset Range: -7 dB to 7 dB, Unit: dB
		"""
		response = self._core.io.query_str('CONFigure:LTE:SIGNaling<Instance>:UL:SETB:PUSCh:TPC:CLTPower:OFFSet?')
		return Conversions.str_to_float(response)

	def set_offset(self, offset: float) -> None:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:UL:SETB:PUSCh:TPC:CLTPower:OFFSet \n
		Snippet: driver.configure.uplink.setb.pusch.tpc.cltPower.set_offset(offset = 1.0) \n
		Defines a target power offset relative to the power master CC, for power control with the TPC setup CLOop. The setting is
		irrelevant for carriers with independent UL power control. \n
			:param offset: Target power = master target power + Offset Range: -7 dB to 7 dB, Unit: dB
		"""
		param = Conversions.decimal_value_to_str(offset)
		self._core.io.write(f'CONFigure:LTE:SIGNaling<Instance>:UL:SETB:PUSCh:TPC:CLTPower:OFFSet {param}')

	def get_value(self) -> float:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:UL:SETB:PUSCh:TPC:CLTPower \n
		Snippet: value: float = driver.configure.uplink.setb.pusch.tpc.cltPower.get_value() \n
		Defines the target power for power control with the TPC setup CLOop. \n
			:return: power: Range: -50 dBm to 33 dBm, Unit: dBm
		"""
		response = self._core.io.query_str('CONFigure:LTE:SIGNaling<Instance>:UL:SETB:PUSCh:TPC:CLTPower?')
		return Conversions.str_to_float(response)

	def set_value(self, power: float) -> None:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:UL:SETB:PUSCh:TPC:CLTPower \n
		Snippet: driver.configure.uplink.setb.pusch.tpc.cltPower.set_value(power = 1.0) \n
		Defines the target power for power control with the TPC setup CLOop. \n
			:param power: Range: -50 dBm to 33 dBm, Unit: dBm
		"""
		param = Conversions.decimal_value_to_str(power)
		self._core.io.write(f'CONFigure:LTE:SIGNaling<Instance>:UL:SETB:PUSCh:TPC:CLTPower {param}')

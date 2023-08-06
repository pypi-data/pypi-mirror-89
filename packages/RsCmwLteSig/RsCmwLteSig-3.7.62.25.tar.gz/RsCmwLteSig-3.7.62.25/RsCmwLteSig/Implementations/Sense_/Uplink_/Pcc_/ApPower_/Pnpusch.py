from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pnpusch:
	"""Pnpusch commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pnpusch", core, parent)

	def get_basic(self) -> float:
		"""SCPI: SENSe:LTE:SIGNaling<instance>:UL[:PCC]:APPower:PNPusch:BASic \n
		Snippet: value: float = driver.sense.uplink.pcc.apPower.pnpusch.get_basic() \n
		Queries the 'p0-NominalPUSCH' value, signaled to the UE if basic UL power configuration applies. \n
			:return: p_0_nominal_pusch: Range: -126 dBm to 24 dBm, Unit: dBm
		"""
		response = self._core.io.query_str('SENSe:LTE:SIGNaling<Instance>:UL:PCC:APPower:PNPusch:BASic?')
		return Conversions.str_to_float(response)

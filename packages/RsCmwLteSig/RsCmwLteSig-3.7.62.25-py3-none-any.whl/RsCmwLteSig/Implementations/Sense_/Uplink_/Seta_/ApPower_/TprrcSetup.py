from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TprrcSetup:
	"""TprrcSetup commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tprrcSetup", core, parent)

	def get_basic(self) -> bool:
		"""SCPI: SENSe:LTE:SIGNaling<instance>:UL:SETA:APPower:TPRRcsetup:BASic \n
		Snippet: value: bool = driver.sense.uplink.seta.apPower.tprrcSetup.get_basic() \n
		Queries the state of P0-UE-PUSCH toggling, determining the P0-UE-PUSCH values signaled to the UE during RRC connection
		setup if basic UL power configuration applies. \n
			:return: enable: OFF | ON
		"""
		response = self._core.io.query_str('SENSe:LTE:SIGNaling<Instance>:UL:SETA:APPower:TPRRcsetup:BASic?')
		return Conversions.str_to_bool(response)

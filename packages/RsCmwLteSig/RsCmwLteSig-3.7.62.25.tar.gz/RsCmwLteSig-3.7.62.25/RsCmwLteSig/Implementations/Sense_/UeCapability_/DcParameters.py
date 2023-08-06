from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DcParameters:
	"""DcParameters commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dcParameters", core, parent)

	def get_dtscg(self) -> bool:
		"""SCPI: SENSe:LTE:SIGNaling<instance>:UECapability:DCParameters:DTSCg \n
		Snippet: value: bool = driver.sense.ueCapability.dcParameters.get_dtscg() \n
		Returns whether the UE supports the DRB type of SCG bearer. \n
			:return: typescg: OFF | ON
		"""
		response = self._core.io.query_str('SENSe:LTE:SIGNaling<Instance>:UECapability:DCParameters:DTSCg?')
		return Conversions.str_to_bool(response)

	def get_dt_split(self) -> bool:
		"""SCPI: SENSe:LTE:SIGNaling<instance>:UECapability:DCParameters:DTSPlit \n
		Snippet: value: bool = driver.sense.ueCapability.dcParameters.get_dt_split() \n
		Returns whether the UE supports the DRB type of split bearer. \n
			:return: typesplit: OFF | ON
		"""
		response = self._core.io.query_str('SENSe:LTE:SIGNaling<Instance>:UECapability:DCParameters:DTSPlit?')
		return Conversions.str_to_bool(response)

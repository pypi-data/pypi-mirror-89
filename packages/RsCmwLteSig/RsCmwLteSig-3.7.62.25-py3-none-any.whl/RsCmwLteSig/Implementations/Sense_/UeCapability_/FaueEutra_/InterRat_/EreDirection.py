from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EreDirection:
	"""EreDirection commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ereDirection", core, parent)

	def get_utra(self) -> bool:
		"""SCPI: SENSe:LTE:SIGNaling<instance>:UECapability:FAUeeutra:IRAT:EREDirection:UTRA \n
		Snippet: value: bool = driver.sense.ueCapability.faueEutra.interRat.ereDirection.get_utra() \n
		Returns whether the UE supports an enhanced redirection to UTRA FDD or not. \n
			:return: supported: OFF | ON
		"""
		response = self._core.io.query_str('SENSe:LTE:SIGNaling<Instance>:UECapability:FAUeeutra:IRAT:EREDirection:UTRA?')
		return Conversions.str_to_bool(response)

	def get_utdd(self) -> bool:
		"""SCPI: SENSe:LTE:SIGNaling<instance>:UECapability:FAUeeutra:IRAT:EREDirection:UTDD \n
		Snippet: value: bool = driver.sense.ueCapability.faueEutra.interRat.ereDirection.get_utdd() \n
		Returns whether the UE supports an enhanced redirection to UTRA TDD or not. \n
			:return: supported: OFF | ON
		"""
		response = self._core.io.query_str('SENSe:LTE:SIGNaling<Instance>:UECapability:FAUeeutra:IRAT:EREDirection:UTDD?')
		return Conversions.str_to_bool(response)

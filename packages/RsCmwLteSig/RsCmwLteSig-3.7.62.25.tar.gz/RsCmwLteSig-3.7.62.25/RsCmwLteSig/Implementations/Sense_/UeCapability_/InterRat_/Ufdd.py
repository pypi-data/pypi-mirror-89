from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ufdd:
	"""Ufdd commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ufdd", core, parent)

	@property
	def ereDirection(self):
		"""ereDirection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ereDirection'):
			from .Ufdd_.EreDirection import EreDirection
			self._ereDirection = EreDirection(self._core, self._base)
		return self._ereDirection

	def get_supported(self) -> List[bool]:
		"""SCPI: SENSe:LTE:SIGNaling<instance>:UECapability:IRAT:UFDD:SUPPorted \n
		Snippet: value: List[bool] = driver.sense.ueCapability.interRat.ufdd.get_supported() \n
		Returns a list of values indicating the support of the individual UTRA FDD operating bands by the UE. \n
			:return: supported_band: OFF | ON 32 values: band 1, ..., band 32
		"""
		response = self._core.io.query_str('SENSe:LTE:SIGNaling<Instance>:UECapability:IRAT:UFDD:SUPPorted?')
		return Conversions.str_to_bool_list(response)

	def clone(self) -> 'Ufdd':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ufdd(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

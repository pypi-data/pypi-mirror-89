from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class V:
	"""V commands group definition. 7 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("v", core, parent)

	@property
	def eutra(self):
		"""eutra commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_eutra'):
			from .V_.Eutra import Eutra
			self._eutra = Eutra(self._core, self._base)
		return self._eutra

	def get_bcset(self) -> List[str]:
		"""SCPI: SENSe:LTE:SIGNaling<instance>:UECapability:RF:BCOMbination:V<Number>:BCSet \n
		Snippet: value: List[str] = driver.sense.ueCapability.rf.bcombination.v.get_bcset() \n
		Returns a list of binary numbers, indicating which bandwidth combination sets the UE supports for the individual carrier
		aggregation band combinations. \n
			:return: band: Comma-separated list of binary numbers, one binary number per band combination (combination 0 to n) Each binary number indicates which bandwidth combination sets are supported for the band combination. The leftmost bit corresponds to set 0, the next bit to set 1, and so on. '0' means not supported. '1' means supported.
		"""
		response = self._core.io.query_str('SENSe:LTE:SIGNaling<Instance>:UECapability:RF:BCOMbination:V1020:BCSet?')
		return Conversions.str_to_str_list(response)

	def clone(self) -> 'V':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = V(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

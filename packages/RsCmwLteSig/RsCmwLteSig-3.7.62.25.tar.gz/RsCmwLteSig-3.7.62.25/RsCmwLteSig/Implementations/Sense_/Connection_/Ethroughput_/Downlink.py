from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Downlink:
	"""Downlink commands group definition. 5 total commands, 2 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("downlink", core, parent)

	@property
	def pcc(self):
		"""pcc commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_pcc'):
			from .Downlink_.Pcc import Pcc
			self._pcc = Pcc(self._core, self._base)
		return self._pcc

	@property
	def scc(self):
		"""scc commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_scc'):
			from .Downlink_.Scc import Scc
			self._scc = Scc(self._core, self._base)
		return self._scc

	def get_all(self) -> float:
		"""SCPI: SENSe:LTE:SIGNaling<instance>:CONNection:ETHRoughput:DL:ALL \n
		Snippet: value: float = driver.sense.connection.ethroughput.downlink.get_all() \n
		Returns the expected maximum throughput (averaged over one frame) for the sum of all DL streams of all component carriers.
		The throughput is calculated for the currently selected scheduling type. \n
			:return: throughput: Unit: Mbit/s
		"""
		response = self._core.io.query_str('SENSe:LTE:SIGNaling<Instance>:CONNection:ETHRoughput:DL:ALL?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'Downlink':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Downlink(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

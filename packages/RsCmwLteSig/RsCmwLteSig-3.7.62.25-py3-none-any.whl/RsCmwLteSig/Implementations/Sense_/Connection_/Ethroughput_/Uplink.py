from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Uplink:
	"""Uplink commands group definition. 3 total commands, 1 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("uplink", core, parent)

	@property
	def scc(self):
		"""scc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scc'):
			from .Uplink_.Scc import Scc
			self._scc = Scc(self._core, self._base)
		return self._scc

	def get_pcc(self) -> float:
		"""SCPI: SENSe:LTE:SIGNaling<instance>:CONNection:ETHRoughput:UL[:PCC] \n
		Snippet: value: float = driver.sense.connection.ethroughput.uplink.get_pcc() \n
		Returns the expected maximum throughput (averaged over one frame) for the uplink of one component carrier. The throughput
		is calculated for the currently selected scheduling type. \n
			:return: throughput: Unit: Mbit/s
		"""
		response = self._core.io.query_str('SENSe:LTE:SIGNaling<Instance>:CONNection:ETHRoughput:UL:PCC?')
		return Conversions.str_to_float(response)

	def get_all(self) -> float:
		"""SCPI: SENSe:LTE:SIGNaling<instance>:CONNection:ETHRoughput:UL:ALL \n
		Snippet: value: float = driver.sense.connection.ethroughput.uplink.get_all() \n
		Returns the expected maximum uplink throughput (averaged over one frame) for the sum of all component carriers.
		The throughput is calculated for the currently selected scheduling type. \n
			:return: throughput: Unit: Mbit/s
		"""
		response = self._core.io.query_str('SENSe:LTE:SIGNaling<Instance>:CONNection:ETHRoughput:UL:ALL?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'Uplink':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Uplink(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

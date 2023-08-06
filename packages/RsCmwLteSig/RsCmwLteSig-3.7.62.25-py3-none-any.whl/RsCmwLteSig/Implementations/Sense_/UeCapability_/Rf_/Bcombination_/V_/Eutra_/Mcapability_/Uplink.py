from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Uplink:
	"""Uplink commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("uplink", core, parent)

	def get(self, eutraBand=repcap.EutraBand.Default) -> List[int]:
		"""SCPI: SENSe:LTE:SIGNaling<instance>:UECapability:RF:BCOMbination:V<Number>:EUTRa<BandNr>:MCAPability:UL \n
		Snippet: value: List[int] = driver.sense.ueCapability.rf.bcombination.v.eutra.mcapability.uplink.get(eutraBand = repcap.EutraBand.Default) \n
		Returns the number of layers supported by the UE for spatial multiplexing in the uplink or downlink. The information is
		returned for a selected band of all supported carrier aggregation band combinations. \n
			:param eutraBand: optional repeated capability selector. Default value: Band1 (settable in the interface 'Eutra')
			:return: mimo_capability: Comma-separated list of numbers, 26 numbers per band combination (combination 0 to n) The 26 numbers indicate the supported number of layers for bandwidth class 'a' to 'z'."""
		eutraBand_cmd_val = self._base.get_repcap_cmd_value(eutraBand, repcap.EutraBand)
		response = self._core.io.query_bin_or_ascii_int_list(f'SENSe:LTE:SIGNaling<Instance>:UECapability:RF:BCOMbination:V1020:EUTRa{eutraBand_cmd_val}:MCAPability:UL?')
		return response

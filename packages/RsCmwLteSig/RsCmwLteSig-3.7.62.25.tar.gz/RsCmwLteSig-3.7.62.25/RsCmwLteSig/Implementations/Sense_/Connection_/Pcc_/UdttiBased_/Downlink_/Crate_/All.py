from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class All:
	"""All commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("all", core, parent)

	def get(self, stream=repcap.Stream.Default) -> List[float]:
		"""SCPI: SENSe:LTE:SIGNaling<instance>:CONNection[:PCC]:UDTTibased:DL<Stream>:CRATe:ALL \n
		Snippet: value: List[float] = driver.sense.connection.pcc.udttiBased.downlink.crate.all.get(stream = repcap.Stream.Default) \n
		Queries the code rate for all downlink subframes for the scheduling type 'User-defined TTI-Based'. \n
			:param stream: optional repeated capability selector. Default value: S1 (settable in the interface 'Downlink')
			:return: code_rate: Comma-separated list of 10 values (subframe 0 to subframe 9) Range: 0 to 50"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_bin_or_ascii_float_list(f'SENSe:LTE:SIGNaling<Instance>:CONNection:PCC:UDTTibased:DL{stream_cmd_val}:CRATe:ALL?')
		return response

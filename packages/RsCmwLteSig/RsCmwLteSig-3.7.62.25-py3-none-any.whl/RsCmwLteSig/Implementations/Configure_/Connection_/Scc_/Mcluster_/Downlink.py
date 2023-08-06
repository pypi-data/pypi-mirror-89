from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Downlink:
	"""Downlink commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("downlink", core, parent)

	def set(self, multicluster: bool, secondaryCompCarrier=repcap.SecondaryCompCarrier.Default) -> None:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:CONNection:SCC<carrier>:MCLuster:DL \n
		Snippet: driver.configure.connection.scc.mcluster.downlink.set(multicluster = False, secondaryCompCarrier = repcap.SecondaryCompCarrier.Default) \n
		Enables/disables multi-cluster allocation for the DL. \n
			:param multicluster: OFF | ON OFF: contiguous allocation ON: multi-cluster allocation
			:param secondaryCompCarrier: optional repeated capability selector. Default value: CC1 (settable in the interface 'Scc')"""
		param = Conversions.bool_to_str(multicluster)
		secondaryCompCarrier_cmd_val = self._base.get_repcap_cmd_value(secondaryCompCarrier, repcap.SecondaryCompCarrier)
		self._core.io.write(f'CONFigure:LTE:SIGNaling<Instance>:CONNection:SCC{secondaryCompCarrier_cmd_val}:MCLuster:DL {param}')

	def get(self, secondaryCompCarrier=repcap.SecondaryCompCarrier.Default) -> bool:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:CONNection:SCC<carrier>:MCLuster:DL \n
		Snippet: value: bool = driver.configure.connection.scc.mcluster.downlink.get(secondaryCompCarrier = repcap.SecondaryCompCarrier.Default) \n
		Enables/disables multi-cluster allocation for the DL. \n
			:param secondaryCompCarrier: optional repeated capability selector. Default value: CC1 (settable in the interface 'Scc')
			:return: multicluster: OFF | ON OFF: contiguous allocation ON: multi-cluster allocation"""
		secondaryCompCarrier_cmd_val = self._base.get_repcap_cmd_value(secondaryCompCarrier, repcap.SecondaryCompCarrier)
		response = self._core.io.query_str(f'CONFigure:LTE:SIGNaling<Instance>:CONNection:SCC{secondaryCompCarrier_cmd_val}:MCLuster:DL?')
		return Conversions.str_to_bool(response)

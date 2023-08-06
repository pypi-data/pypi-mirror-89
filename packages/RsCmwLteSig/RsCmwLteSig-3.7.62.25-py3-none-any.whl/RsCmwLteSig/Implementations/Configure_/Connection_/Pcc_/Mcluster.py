from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mcluster:
	"""Mcluster commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mcluster", core, parent)

	def get_uplink(self) -> bool:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:CONNection[:PCC]:MCLuster:UL \n
		Snippet: value: bool = driver.configure.connection.pcc.mcluster.get_uplink() \n
		Enables/disables multi-cluster allocation for the UL. \n
			:return: multicluster: OFF | ON OFF: contiguous allocation, resource allocation type 0 ON: multi-cluster allocation, resource allocation type 1
		"""
		response = self._core.io.query_str('CONFigure:LTE:SIGNaling<Instance>:CONNection:PCC:MCLuster:UL?')
		return Conversions.str_to_bool(response)

	def set_uplink(self, multicluster: bool) -> None:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:CONNection[:PCC]:MCLuster:UL \n
		Snippet: driver.configure.connection.pcc.mcluster.set_uplink(multicluster = False) \n
		Enables/disables multi-cluster allocation for the UL. \n
			:param multicluster: OFF | ON OFF: contiguous allocation, resource allocation type 0 ON: multi-cluster allocation, resource allocation type 1
		"""
		param = Conversions.bool_to_str(multicluster)
		self._core.io.write(f'CONFigure:LTE:SIGNaling<Instance>:CONNection:PCC:MCLuster:UL {param}')

	def get_downlink(self) -> bool:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:CONNection[:PCC]:MCLuster:DL \n
		Snippet: value: bool = driver.configure.connection.pcc.mcluster.get_downlink() \n
		Enables/disables multi-cluster allocation for the DL. \n
			:return: multicluster: OFF | ON OFF: contiguous allocation ON: multi-cluster allocation
		"""
		response = self._core.io.query_str('CONFigure:LTE:SIGNaling<Instance>:CONNection:PCC:MCLuster:DL?')
		return Conversions.str_to_bool(response)

	def set_downlink(self, multicluster: bool) -> None:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:CONNection[:PCC]:MCLuster:DL \n
		Snippet: driver.configure.connection.pcc.mcluster.set_downlink(multicluster = False) \n
		Enables/disables multi-cluster allocation for the DL. \n
			:param multicluster: OFF | ON OFF: contiguous allocation ON: multi-cluster allocation
		"""
		param = Conversions.bool_to_str(multicluster)
		self._core.io.write(f'CONFigure:LTE:SIGNaling<Instance>:CONNection:PCC:MCLuster:DL {param}')

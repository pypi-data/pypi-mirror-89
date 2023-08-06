from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class McsTable:
	"""McsTable commands group definition. 3 total commands, 2 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mcsTable", core, parent)

	@property
	def csirs(self):
		"""csirs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_csirs'):
			from .McsTable_.Csirs import Csirs
			self._csirs = Csirs(self._core, self._base)
		return self._csirs

	@property
	def ssubframe(self):
		"""ssubframe commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ssubframe'):
			from .McsTable_.Ssubframe import Ssubframe
			self._ssubframe = Ssubframe(self._core, self._base)
		return self._ssubframe

	def get_user_defined(self) -> List[int]:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:CONNection[:PCC]:FCPRi:DL:MCSTable:UDEFined \n
		Snippet: value: List[int] = driver.configure.connection.pcc.fcpri.downlink.mcsTable.get_user_defined() \n
		Configures a user-defined mapping table that assigns an MCS index value to each possible reported wideband CQI index
		value. The table is used for the scheduling type 'Follow WB CQI-PMI-RI' if the table mode is set to UDEFined. \n
			:return: mcs: Comma-separated list of 15 MCS values, for reported CQI index value 1 to 15 Range: 0 to 28
		"""
		response = self._core.io.query_bin_or_ascii_int_list('CONFigure:LTE:SIGNaling<Instance>:CONNection:PCC:FCPRi:DL:MCSTable:UDEFined?')
		return response

	def set_user_defined(self, mcs: List[int]) -> None:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:CONNection[:PCC]:FCPRi:DL:MCSTable:UDEFined \n
		Snippet: driver.configure.connection.pcc.fcpri.downlink.mcsTable.set_user_defined(mcs = [1, 2, 3]) \n
		Configures a user-defined mapping table that assigns an MCS index value to each possible reported wideband CQI index
		value. The table is used for the scheduling type 'Follow WB CQI-PMI-RI' if the table mode is set to UDEFined. \n
			:param mcs: Comma-separated list of 15 MCS values, for reported CQI index value 1 to 15 Range: 0 to 28
		"""
		param = Conversions.list_to_csv_str(mcs)
		self._core.io.write(f'CONFigure:LTE:SIGNaling<Instance>:CONNection:PCC:FCPRi:DL:MCSTable:UDEFined {param}')

	def clone(self) -> 'McsTable':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = McsTable(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

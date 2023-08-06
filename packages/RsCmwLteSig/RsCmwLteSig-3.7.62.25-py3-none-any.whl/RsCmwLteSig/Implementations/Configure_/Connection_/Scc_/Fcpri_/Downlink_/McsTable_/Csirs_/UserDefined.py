from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UserDefined:
	"""UserDefined commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("userDefined", core, parent)

	def set(self, mcs: List[int], secondaryCompCarrier=repcap.SecondaryCompCarrier.Default) -> None:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:CONNection:SCC<Carrier>:FCPRi:DL:MCSTable:CSIRs:UDEFined \n
		Snippet: driver.configure.connection.scc.fcpri.downlink.mcsTable.csirs.userDefined.set(mcs = [1, 2, 3], secondaryCompCarrier = repcap.SecondaryCompCarrier.Default) \n
		Configures a user-defined mapping table for subframes with CSI-RS that assigns an MCS index value to each possible
		reported wideband CQI index value. The table is used for the scheduling type 'Follow WB CQI-PMI-RI' if the table mode is
		set to UDEFined. \n
			:param mcs: Comma-separated list of 15 MCS values, for reported CQI index value 1 to 15 Range: 0 to 28
			:param secondaryCompCarrier: optional repeated capability selector. Default value: CC1 (settable in the interface 'Scc')"""
		param = Conversions.list_to_csv_str(mcs)
		secondaryCompCarrier_cmd_val = self._base.get_repcap_cmd_value(secondaryCompCarrier, repcap.SecondaryCompCarrier)
		self._core.io.write(f'CONFigure:LTE:SIGNaling<Instance>:CONNection:SCC{secondaryCompCarrier_cmd_val}:FCPRi:DL:MCSTable:CSIRs:UDEFined {param}')

	def get(self, secondaryCompCarrier=repcap.SecondaryCompCarrier.Default) -> List[int]:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:CONNection:SCC<Carrier>:FCPRi:DL:MCSTable:CSIRs:UDEFined \n
		Snippet: value: List[int] = driver.configure.connection.scc.fcpri.downlink.mcsTable.csirs.userDefined.get(secondaryCompCarrier = repcap.SecondaryCompCarrier.Default) \n
		Configures a user-defined mapping table for subframes with CSI-RS that assigns an MCS index value to each possible
		reported wideband CQI index value. The table is used for the scheduling type 'Follow WB CQI-PMI-RI' if the table mode is
		set to UDEFined. \n
			:param secondaryCompCarrier: optional repeated capability selector. Default value: CC1 (settable in the interface 'Scc')
			:return: mcs: Comma-separated list of 15 MCS values, for reported CQI index value 1 to 15 Range: 0 to 28"""
		secondaryCompCarrier_cmd_val = self._base.get_repcap_cmd_value(secondaryCompCarrier, repcap.SecondaryCompCarrier)
		response = self._core.io.query_bin_or_ascii_int_list(f'CONFigure:LTE:SIGNaling<Instance>:CONNection:SCC{secondaryCompCarrier_cmd_val}:FCPRi:DL:MCSTable:CSIRs:UDEFined?')
		return response

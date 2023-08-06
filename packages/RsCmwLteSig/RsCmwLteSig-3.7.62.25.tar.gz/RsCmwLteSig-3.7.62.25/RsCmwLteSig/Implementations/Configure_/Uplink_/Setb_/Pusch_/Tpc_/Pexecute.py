from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pexecute:
	"""Pexecute commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pexecute", core, parent)

	def set(self) -> None:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:UL:SETB:PUSCh:TPC:PEXecute \n
		Snippet: driver.configure.uplink.setb.pusch.tpc.pexecute.set() \n
		Execute the active TPC setup for power control of the PUSCH. This command is only relevant for setups which are not
		executed automatically (SINGle, UDSingle, RPControl, FULPower) . \n
		"""
		self._core.io.write(f'CONFigure:LTE:SIGNaling<Instance>:UL:SETB:PUSCh:TPC:PEXecute')

	def set_with_opc(self) -> None:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:UL:SETB:PUSCh:TPC:PEXecute \n
		Snippet: driver.configure.uplink.setb.pusch.tpc.pexecute.set_with_opc() \n
		Execute the active TPC setup for power control of the PUSCH. This command is only relevant for setups which are not
		executed automatically (SINGle, UDSingle, RPControl, FULPower) . \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCmwLteSig.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'CONFigure:LTE:SIGNaling<Instance>:UL:SETB:PUSCh:TPC:PEXecute')

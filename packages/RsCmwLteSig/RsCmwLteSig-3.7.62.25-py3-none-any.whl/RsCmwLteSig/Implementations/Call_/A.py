from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class A:
	"""A commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("a", core, parent)

	def set_action(self, scc_action: enums.SccAction) -> None:
		"""SCPI: CALL:LTE:SIGNaling<instance>:A:ACTion \n
		Snippet: driver.call.a.set_action(scc_action = enums.SccAction.MACactivate) \n
		Control the state of all SCCs assigned to the synchronization set A or B. \n
			:param scc_action: OFF | ON | RRCadd | MACactivate | MACDeactivat | RRCDelete OFF: Switch off SCC ON: Switch on SCC RRCadd: Add SCC RRC connection MACactivate: Activate MAC for the SCC MACDeactivat: Deactivate MAC for the SCC RRCDelete: Delete SCC RRC connection
		"""
		param = Conversions.enum_scalar_to_str(scc_action, enums.SccAction)
		self._core.io.write_with_opc(f'CALL:LTE:SIGNaling<Instance>:A:ACTion {param}')

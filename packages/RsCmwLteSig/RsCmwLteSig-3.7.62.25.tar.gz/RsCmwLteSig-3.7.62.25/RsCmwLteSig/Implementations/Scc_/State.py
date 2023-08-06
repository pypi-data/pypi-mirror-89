from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	# noinspection PyTypeChecker
	def fetch(self, secondaryCompCarrier=repcap.SecondaryCompCarrier.Default) -> enums.SyncState:
		"""SCPI: FETCh:LTE:SIGNaling<instance>:SCC<Carrier>:STATe \n
		Snippet: value: enums.SyncState = driver.scc.state.fetch(secondaryCompCarrier = repcap.SecondaryCompCarrier.Default) \n
		Queries the state of the SCC number <c>, see also 'SCC States'. \n
			:param secondaryCompCarrier: optional repeated capability selector. Default value: CC1 (settable in the interface 'Scc')
			:return: scc_state: OFF | ON | RRCadded | MACactivated OFF: SCC off ON: SCC on RRCadded: RRC added MACactivated: MAC activated"""
		secondaryCompCarrier_cmd_val = self._base.get_repcap_cmd_value(secondaryCompCarrier, repcap.SecondaryCompCarrier)
		response = self._core.io.query_str(f'FETCh:LTE:SIGNaling<Instance>:SCC{secondaryCompCarrier_cmd_val}:STATe?')
		return Conversions.str_to_scalar_enum(response, enums.SyncState)

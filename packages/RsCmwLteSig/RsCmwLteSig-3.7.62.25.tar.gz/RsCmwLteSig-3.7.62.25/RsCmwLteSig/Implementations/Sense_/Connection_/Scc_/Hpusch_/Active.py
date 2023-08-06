from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Active:
	"""Active commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("active", core, parent)

	def get(self, secondaryCompCarrier=repcap.SecondaryCompCarrier.Default) -> bool:
		"""SCPI: SENSe:LTE:SIGNaling<instance>:CONNection:SCC<Carrier>:HPUSch:ACTive \n
		Snippet: value: bool = driver.sense.connection.scc.hpusch.active.get(secondaryCompCarrier = repcap.SecondaryCompCarrier.Default) \n
		Queries whether PUSCH frequency hopping is active. \n
			:param secondaryCompCarrier: optional repeated capability selector. Default value: CC1 (settable in the interface 'Scc')
			:return: active: OFF | ON"""
		secondaryCompCarrier_cmd_val = self._base.get_repcap_cmd_value(secondaryCompCarrier, repcap.SecondaryCompCarrier)
		response = self._core.io.query_str(f'SENSe:LTE:SIGNaling<Instance>:CONNection:SCC{secondaryCompCarrier_cmd_val}:HPUSch:ACTive?')
		return Conversions.str_to_bool(response)

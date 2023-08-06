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

	def set(self, offset: int, secondaryCompCarrier=repcap.SecondaryCompCarrier.Default) -> None:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:RFSettings:SCC<Carrier>:FOFFset:DL \n
		Snippet: driver.configure.rfSettings.scc.freqOffset.downlink.set(offset = 1, secondaryCompCarrier = repcap.SecondaryCompCarrier.Default) \n
		Specifies a positive or negative frequency offset to be added to the center frequency of the configured downlink channel.
		You can use the PCC command to configure the same offset for the PCC and all SCCs. Or you can use the PCC and SCC command
		to configure different values. See also CONFigure:LTE:SIGN<i>:FOFFset:DL:UCSPecific. \n
			:param offset: Range: -100 kHz to 100 kHz, Unit: Hz
			:param secondaryCompCarrier: optional repeated capability selector. Default value: CC1 (settable in the interface 'Scc')"""
		param = Conversions.decimal_value_to_str(offset)
		secondaryCompCarrier_cmd_val = self._base.get_repcap_cmd_value(secondaryCompCarrier, repcap.SecondaryCompCarrier)
		self._core.io.write_with_opc(f'CONFigure:LTE:SIGNaling<Instance>:RFSettings:SCC{secondaryCompCarrier_cmd_val}:FOFFset:DL {param}')

	def get(self, secondaryCompCarrier=repcap.SecondaryCompCarrier.Default) -> int:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:RFSettings:SCC<Carrier>:FOFFset:DL \n
		Snippet: value: int = driver.configure.rfSettings.scc.freqOffset.downlink.get(secondaryCompCarrier = repcap.SecondaryCompCarrier.Default) \n
		Specifies a positive or negative frequency offset to be added to the center frequency of the configured downlink channel.
		You can use the PCC command to configure the same offset for the PCC and all SCCs. Or you can use the PCC and SCC command
		to configure different values. See also CONFigure:LTE:SIGN<i>:FOFFset:DL:UCSPecific. \n
			:param secondaryCompCarrier: optional repeated capability selector. Default value: CC1 (settable in the interface 'Scc')
			:return: offset: Range: -100 kHz to 100 kHz, Unit: Hz"""
		secondaryCompCarrier_cmd_val = self._base.get_repcap_cmd_value(secondaryCompCarrier, repcap.SecondaryCompCarrier)
		response = self._core.io.query_str_with_opc(f'CONFigure:LTE:SIGNaling<Instance>:RFSettings:SCC{secondaryCompCarrier_cmd_val}:FOFFset:DL?')
		return Conversions.str_to_int(response)

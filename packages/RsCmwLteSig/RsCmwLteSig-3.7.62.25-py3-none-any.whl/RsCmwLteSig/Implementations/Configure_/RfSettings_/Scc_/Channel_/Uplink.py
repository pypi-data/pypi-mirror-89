from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Uplink:
	"""Uplink commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("uplink", core, parent)

	def set(self, channel: int, secondaryCompCarrier=repcap.SecondaryCompCarrier.Default) -> None:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:RFSettings:SCC<Carrier>:CHANnel:UL \n
		Snippet: driver.configure.rfSettings.scc.channel.uplink.set(channel = 1, secondaryCompCarrier = repcap.SecondaryCompCarrier.Default) \n
		Selects the UL channel number. It must be valid for the current operating band. The related DL channel number is
		calculated and set automatically. By appending a Hz unit (e.g. Hz, kHz, MHz) to a setting command, you can set the
		channel via its center frequency (only integer numbers accepted) . By appending a Hz unit to a query command, you can
		query the center frequency instead of the channel number. For channel numbers and frequencies depending on operating
		bands, see 'Operating Bands'. \n
			:param channel: Range: depends on operating band
			:param secondaryCompCarrier: optional repeated capability selector. Default value: CC1 (settable in the interface 'Scc')"""
		param = Conversions.decimal_value_to_str(channel)
		secondaryCompCarrier_cmd_val = self._base.get_repcap_cmd_value(secondaryCompCarrier, repcap.SecondaryCompCarrier)
		self._core.io.write_with_opc(f'CONFigure:LTE:SIGNaling<Instance>:RFSettings:SCC{secondaryCompCarrier_cmd_val}:CHANnel:UL {param}')

	def get(self, secondaryCompCarrier=repcap.SecondaryCompCarrier.Default) -> int:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:RFSettings:SCC<Carrier>:CHANnel:UL \n
		Snippet: value: int = driver.configure.rfSettings.scc.channel.uplink.get(secondaryCompCarrier = repcap.SecondaryCompCarrier.Default) \n
		Selects the UL channel number. It must be valid for the current operating band. The related DL channel number is
		calculated and set automatically. By appending a Hz unit (e.g. Hz, kHz, MHz) to a setting command, you can set the
		channel via its center frequency (only integer numbers accepted) . By appending a Hz unit to a query command, you can
		query the center frequency instead of the channel number. For channel numbers and frequencies depending on operating
		bands, see 'Operating Bands'. \n
			:param secondaryCompCarrier: optional repeated capability selector. Default value: CC1 (settable in the interface 'Scc')
			:return: channel: Range: depends on operating band"""
		secondaryCompCarrier_cmd_val = self._base.get_repcap_cmd_value(secondaryCompCarrier, repcap.SecondaryCompCarrier)
		response = self._core.io.query_str_with_opc(f'CONFigure:LTE:SIGNaling<Instance>:RFSettings:SCC{secondaryCompCarrier_cmd_val}:CHANnel:UL?')
		return Conversions.str_to_int(response)

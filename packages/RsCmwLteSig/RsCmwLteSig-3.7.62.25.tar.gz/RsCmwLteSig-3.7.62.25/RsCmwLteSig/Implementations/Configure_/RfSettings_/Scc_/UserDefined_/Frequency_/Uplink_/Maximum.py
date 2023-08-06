from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Maximum:
	"""Maximum commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("maximum", core, parent)

	def get(self, secondaryCompCarrier=repcap.SecondaryCompCarrier.Default) -> int:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:RFSettings:SCC<Carrier>:UDEFined:FREQuency:UL:MAXimum \n
		Snippet: value: int = driver.configure.rfSettings.scc.userDefined.frequency.uplink.maximum.get(secondaryCompCarrier = repcap.SecondaryCompCarrier.Default) \n
		Query the minimum and maximum uplink carrier center frequencies resulting from the user-defined band settings.
		For calculations, see CONFigure:LTE:SIGN<i>:UDEFined:FREQuency:DL:MINimum. \n
			:param secondaryCompCarrier: optional repeated capability selector. Default value: CC1 (settable in the interface 'Scc')
			:return: frequency: Range: 70 MHz to 6 GHz, Unit: Hz"""
		secondaryCompCarrier_cmd_val = self._base.get_repcap_cmd_value(secondaryCompCarrier, repcap.SecondaryCompCarrier)
		response = self._core.io.query_str(f'CONFigure:LTE:SIGNaling<Instance>:RFSettings:SCC{secondaryCompCarrier_cmd_val}:UDEFined:FREQuency:UL:MAXimum?')
		return Conversions.str_to_int(response)

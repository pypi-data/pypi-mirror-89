from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Advanced:
	"""Advanced commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("advanced", core, parent)

	def set(self, ref_signal_power: float, secondaryCompCarrier=repcap.SecondaryCompCarrier.Default) -> None:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:UL:SCC<Carrier>:APPower:RSPower:ADVanced \n
		Snippet: driver.configure.uplink.scc.apPower.rsPower.advanced.set(ref_signal_power = 1.0, secondaryCompCarrier = repcap.SecondaryCompCarrier.Default) \n
		Specifies the 'referenceSignalPower' value, signaled to the UE if advanced UL power configuration applies. \n
			:param ref_signal_power: Range: -60 dBm to 50 dBm, Unit: dBm
			:param secondaryCompCarrier: optional repeated capability selector. Default value: CC1 (settable in the interface 'Scc')"""
		param = Conversions.decimal_value_to_str(ref_signal_power)
		secondaryCompCarrier_cmd_val = self._base.get_repcap_cmd_value(secondaryCompCarrier, repcap.SecondaryCompCarrier)
		self._core.io.write(f'CONFigure:LTE:SIGNaling<Instance>:UL:SCC{secondaryCompCarrier_cmd_val}:APPower:RSPower:ADVanced {param}')

	def get(self, secondaryCompCarrier=repcap.SecondaryCompCarrier.Default) -> float:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:UL:SCC<Carrier>:APPower:RSPower:ADVanced \n
		Snippet: value: float = driver.configure.uplink.scc.apPower.rsPower.advanced.get(secondaryCompCarrier = repcap.SecondaryCompCarrier.Default) \n
		Specifies the 'referenceSignalPower' value, signaled to the UE if advanced UL power configuration applies. \n
			:param secondaryCompCarrier: optional repeated capability selector. Default value: CC1 (settable in the interface 'Scc')
			:return: ref_signal_power: Range: -60 dBm to 50 dBm, Unit: dBm"""
		secondaryCompCarrier_cmd_val = self._base.get_repcap_cmd_value(secondaryCompCarrier, repcap.SecondaryCompCarrier)
		response = self._core.io.query_str(f'CONFigure:LTE:SIGNaling<Instance>:UL:SCC{secondaryCompCarrier_cmd_val}:APPower:RSPower:ADVanced?')
		return Conversions.str_to_float(response)

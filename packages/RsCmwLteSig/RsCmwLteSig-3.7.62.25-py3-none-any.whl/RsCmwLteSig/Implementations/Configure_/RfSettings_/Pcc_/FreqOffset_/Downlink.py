from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Downlink:
	"""Downlink commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("downlink", core, parent)

	def get_uc_specific(self) -> bool:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:RFSettings[:PCC]:FOFFset:DL:UCSPecific \n
		Snippet: value: bool = driver.configure.rfSettings.pcc.freqOffset.downlink.get_uc_specific() \n
		Enables or disables the usage of different frequency offset values for the individual downlink or uplink component
		carriers. \n
			:return: enable: OFF | ON OFF: The configured PCC offset is also used for the SCCs. The configured SCC offsets have no effect. ON: You can configure the frequency offset per carrier.
		"""
		response = self._core.io.query_str_with_opc('CONFigure:LTE:SIGNaling<Instance>:RFSettings:PCC:FOFFset:DL:UCSPecific?')
		return Conversions.str_to_bool(response)

	def set_uc_specific(self, enable: bool) -> None:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:RFSettings[:PCC]:FOFFset:DL:UCSPecific \n
		Snippet: driver.configure.rfSettings.pcc.freqOffset.downlink.set_uc_specific(enable = False) \n
		Enables or disables the usage of different frequency offset values for the individual downlink or uplink component
		carriers. \n
			:param enable: OFF | ON OFF: The configured PCC offset is also used for the SCCs. The configured SCC offsets have no effect. ON: You can configure the frequency offset per carrier.
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write_with_opc(f'CONFigure:LTE:SIGNaling<Instance>:RFSettings:PCC:FOFFset:DL:UCSPecific {param}')

	def get_value(self) -> int:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:RFSettings[:PCC]:FOFFset:DL \n
		Snippet: value: int = driver.configure.rfSettings.pcc.freqOffset.downlink.get_value() \n
		Specifies a positive or negative frequency offset to be added to the center frequency of the configured downlink channel.
		You can use the PCC command to configure the same offset for the PCC and all SCCs. Or you can use the PCC and SCC command
		to configure different values. See also CONFigure:LTE:SIGN<i>:FOFFset:DL:UCSPecific. \n
			:return: offset: Range: -100 kHz to 100 kHz, Unit: Hz
		"""
		response = self._core.io.query_str_with_opc('CONFigure:LTE:SIGNaling<Instance>:RFSettings:PCC:FOFFset:DL?')
		return Conversions.str_to_int(response)

	def set_value(self, offset: int) -> None:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:RFSettings[:PCC]:FOFFset:DL \n
		Snippet: driver.configure.rfSettings.pcc.freqOffset.downlink.set_value(offset = 1) \n
		Specifies a positive or negative frequency offset to be added to the center frequency of the configured downlink channel.
		You can use the PCC command to configure the same offset for the PCC and all SCCs. Or you can use the PCC and SCC command
		to configure different values. See also CONFigure:LTE:SIGN<i>:FOFFset:DL:UCSPecific. \n
			:param offset: Range: -100 kHz to 100 kHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(offset)
		self._core.io.write_with_opc(f'CONFigure:LTE:SIGNaling<Instance>:RFSettings:PCC:FOFFset:DL {param}')

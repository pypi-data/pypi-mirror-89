from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Downlink:
	"""Downlink commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: Stream, default value after init: Stream.S1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("downlink", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_stream_get', 'repcap_stream_set', repcap.Stream.S1)

	def repcap_stream_set(self, enum_value: repcap.Stream) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Stream.Default
		Default value after init: Stream.S1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_stream_get(self) -> repcap.Stream:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def set(self, version: int, stream=repcap.Stream.Default) -> None:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:CONNection[:PCC]:RMC:VERSion:DL<Stream> \n
		Snippet: driver.configure.connection.pcc.rmc.version.downlink.set(version = 1, stream = repcap.Stream.Default) \n
		Selects the version to distinguish ambiguous RMCs. This command is only relevant for certain downlink RMCs for TDD
		multiple antenna configurations, see 'DL RMCs, Multiple TX Antennas (TM 2 to 6) '. \n
			:param version: Range: 0 to 1
			:param stream: optional repeated capability selector. Default value: S1 (settable in the interface 'Downlink')"""
		param = Conversions.decimal_value_to_str(version)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'CONFigure:LTE:SIGNaling<Instance>:CONNection:PCC:RMC:VERSion:DL{stream_cmd_val} {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:CONNection[:PCC]:RMC:VERSion:DL<Stream> \n
		Snippet: value: int = driver.configure.connection.pcc.rmc.version.downlink.get(stream = repcap.Stream.Default) \n
		Selects the version to distinguish ambiguous RMCs. This command is only relevant for certain downlink RMCs for TDD
		multiple antenna configurations, see 'DL RMCs, Multiple TX Antennas (TM 2 to 6) '. \n
			:param stream: optional repeated capability selector. Default value: S1 (settable in the interface 'Downlink')
			:return: version: Range: 0 to 1"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'CONFigure:LTE:SIGNaling<Instance>:CONNection:PCC:RMC:VERSion:DL{stream_cmd_val}?')
		return Conversions.str_to_int(response)

	def clone(self) -> 'Downlink':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Downlink(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

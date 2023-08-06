from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from ..........Internal.Types import DataType
from ..........Internal.StructBase import StructBase
from ..........Internal.ArgStruct import ArgStruct
from ..........Internal.ArgSingleList import ArgSingleList
from ..........Internal.ArgSingle import ArgSingle
from ..........Internal.RepeatedCapability import RepeatedCapability
from .......... import enums
from .......... import repcap


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

	def set(self, symbols: enums.Symbols, cluster: float, modulation: enums.Modulation, trans_block_size_idx: int, secondaryCompCarrier=repcap.SecondaryCompCarrier.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:CONNection:SCC<Carrier>:UDCHannels:LAA:RBURst:PEPSubframes:MCLuster:DL<Stream> \n
		Snippet: driver.configure.connection.scc.udChannels.laa.rburst.pepSubFrames.mcluster.downlink.set(symbols = enums.Symbols.S0, cluster = 1.0, modulation = enums.Modulation.Q1024, trans_block_size_idx = 1, secondaryCompCarrier = repcap.SecondaryCompCarrier.Default, stream = repcap.Stream.Default) \n
		Configures a user-defined downlink channel with multi-cluster allocation, for LAA, random bursts. The <Cluster> setting
		applies to all subframes of the burst and to all DL streams. The <Modulation> and <TransBlockSizeIdx> settings apply to
		partial ending subframes with the specified number of allocated OFDM <Symbols> and DL stream <s>. The allowed input
		ranges have dependencies and are described in the background information, see 'User-Defined Channels for LAA' and
		especially Table 'RBG parameters'. \n
			:param symbols: S6 | S9 | S10 | S11 | S12 Number of OFDM symbols allocated in the ending subframe
			:param cluster: Bitmap, enabling or disabling the individual RBGs 1 means RBG is allocated, 0 means RBG is not allocated The number of bits depends on the cell bandwidth and equals the total number of RBGs. The bitmap starts with RBG 0 (most significant bit) and continues with increasing RBG index / frequency. Example for BW 20 MHz: #B1010100000000000000000011 allocates RBG 0, 2, 4, 23, 24
			:param modulation: QPSK | Q16 | Q64 | Q256 Modulation type QPSK | 16-QAM | 64-QAM | 256-QAM
			:param trans_block_size_idx: Transport block size index
			:param secondaryCompCarrier: optional repeated capability selector. Default value: CC1 (settable in the interface 'Scc')
			:param stream: optional repeated capability selector. Default value: S1 (settable in the interface 'Downlink')"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('symbols', symbols, DataType.Enum), ArgSingle('cluster', cluster, DataType.Float), ArgSingle('modulation', modulation, DataType.Enum), ArgSingle('trans_block_size_idx', trans_block_size_idx, DataType.Integer))
		secondaryCompCarrier_cmd_val = self._base.get_repcap_cmd_value(secondaryCompCarrier, repcap.SecondaryCompCarrier)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'CONFigure:LTE:SIGNaling<Instance>:CONNection:SCC{secondaryCompCarrier_cmd_val}:UDCHannels:LAA:RBURst:PEPSubframes:MCLuster:DL{stream_cmd_val} {param}'.rstrip())

	# noinspection PyTypeChecker
	class GetStruct(StructBase):
		"""Response structure. Fields: \n
			- Cluster: float: Bitmap, enabling or disabling the individual RBGs 1 means RBG is allocated, 0 means RBG is not allocated The number of bits depends on the cell bandwidth and equals the total number of RBGs. The bitmap starts with RBG 0 (most significant bit) and continues with increasing RBG index / frequency. Example for BW 20 MHz: #B1010100000000000000000011 allocates RBG 0, 2, 4, 23, 24
			- Modulation: enums.Modulation: QPSK | Q16 | Q64 | Q256 Modulation type QPSK | 16-QAM | 64-QAM | 256-QAM
			- Trans_Block_Size_Idx: int: Transport block size index"""
		__meta_args_list = [
			ArgStruct.scalar_float('Cluster'),
			ArgStruct.scalar_enum('Modulation', enums.Modulation),
			ArgStruct.scalar_int('Trans_Block_Size_Idx')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Cluster: float = None
			self.Modulation: enums.Modulation = None
			self.Trans_Block_Size_Idx: int = None

	def get(self, symbols: enums.Symbols, secondaryCompCarrier=repcap.SecondaryCompCarrier.Default, stream=repcap.Stream.Default) -> GetStruct:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:CONNection:SCC<Carrier>:UDCHannels:LAA:RBURst:PEPSubframes:MCLuster:DL<Stream> \n
		Snippet: value: GetStruct = driver.configure.connection.scc.udChannels.laa.rburst.pepSubFrames.mcluster.downlink.get(symbols = enums.Symbols.S0, secondaryCompCarrier = repcap.SecondaryCompCarrier.Default, stream = repcap.Stream.Default) \n
		Configures a user-defined downlink channel with multi-cluster allocation, for LAA, random bursts. The <Cluster> setting
		applies to all subframes of the burst and to all DL streams. The <Modulation> and <TransBlockSizeIdx> settings apply to
		partial ending subframes with the specified number of allocated OFDM <Symbols> and DL stream <s>. The allowed input
		ranges have dependencies and are described in the background information, see 'User-Defined Channels for LAA' and
		especially Table 'RBG parameters'. \n
			:param symbols: S6 | S9 | S10 | S11 | S12 Number of OFDM symbols allocated in the ending subframe
			:param secondaryCompCarrier: optional repeated capability selector. Default value: CC1 (settable in the interface 'Scc')
			:param stream: optional repeated capability selector. Default value: S1 (settable in the interface 'Downlink')
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		param = Conversions.enum_scalar_to_str(symbols, enums.Symbols)
		secondaryCompCarrier_cmd_val = self._base.get_repcap_cmd_value(secondaryCompCarrier, repcap.SecondaryCompCarrier)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		return self._core.io.query_struct(f'CONFigure:LTE:SIGNaling<Instance>:CONNection:SCC{secondaryCompCarrier_cmd_val}:UDCHannels:LAA:RBURst:PEPSubframes:MCLuster:DL{stream_cmd_val}? {param}', self.__class__.GetStruct())

	def clone(self) -> 'Downlink':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Downlink(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

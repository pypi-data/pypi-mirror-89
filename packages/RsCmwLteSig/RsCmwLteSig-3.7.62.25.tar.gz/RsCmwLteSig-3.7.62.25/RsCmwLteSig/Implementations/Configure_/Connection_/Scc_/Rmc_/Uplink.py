from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Uplink:
	"""Uplink commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("uplink", core, parent)

	# noinspection PyTypeChecker
	class UplinkStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Number_Rb: enums.NumberRb: ZERO | N1 | N2 | N3 | N4 | N5 | N6 | N7 | N8 | N9 | N10 | N12 | N15 | N16 | N17 | N18 | N20 | N24 | N25 | N27 | N30 | N32 | N36 | N40 | N42 | N45 | N48 | N50 | N54 | N60 | N64 | N72 | N75 | N80 | N81 | N83 | N90 | N92 | N96 | N100 Number of allocated resource blocks
			- Modulation: enums.Modulation: QPSK | Q16 | Q64 | Q256 Modulation type QPSK | 16-QAM | 64-QAM | 256-QAM
			- Trans_Block_Size_Idx: enums.TransBlockSizeIdx: ZERO | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T10 | T11 | T12 | T13 | T14 | T15 | T17 | T18 | T19 | T21 | T22 | T23 | T24 | T25 | T30 | T31 | T32 | T8 | T9 | T16 | T20 | T26 | T27 | T28 | T29 Transport block size index. Use KEEP to select a compatible value."""
		__meta_args_list = [
			ArgStruct.scalar_enum('Number_Rb', enums.NumberRb),
			ArgStruct.scalar_enum('Modulation', enums.Modulation),
			ArgStruct.scalar_enum('Trans_Block_Size_Idx', enums.TransBlockSizeIdx)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Number_Rb: enums.NumberRb = None
			self.Modulation: enums.Modulation = None
			self.Trans_Block_Size_Idx: enums.TransBlockSizeIdx = None

	def set(self, structure: UplinkStruct, secondaryCompCarrier=repcap.SecondaryCompCarrier.Default) -> None:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:CONNection:SCC<Carrier>:RMC:UL \n
		Snippet: driver.configure.connection.scc.rmc.uplink.set(value = [PROPERTY_STRUCT_NAME](), secondaryCompCarrier = repcap.SecondaryCompCarrier.Default) \n
		Configures an uplink reference measurement channel (RMC) with contiguous allocation. Only certain value combinations are
		accepted, see 'Scheduling Type RMC'. \n
			:param structure: for set value, see the help for UplinkStruct structure arguments.
			:param secondaryCompCarrier: optional repeated capability selector. Default value: CC1 (settable in the interface 'Scc')"""
		secondaryCompCarrier_cmd_val = self._base.get_repcap_cmd_value(secondaryCompCarrier, repcap.SecondaryCompCarrier)
		self._core.io.write_struct(f'CONFigure:LTE:SIGNaling<Instance>:CONNection:SCC{secondaryCompCarrier_cmd_val}:RMC:UL', structure)

	def get(self, secondaryCompCarrier=repcap.SecondaryCompCarrier.Default) -> UplinkStruct:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:CONNection:SCC<Carrier>:RMC:UL \n
		Snippet: value: UplinkStruct = driver.configure.connection.scc.rmc.uplink.get(secondaryCompCarrier = repcap.SecondaryCompCarrier.Default) \n
		Configures an uplink reference measurement channel (RMC) with contiguous allocation. Only certain value combinations are
		accepted, see 'Scheduling Type RMC'. \n
			:param secondaryCompCarrier: optional repeated capability selector. Default value: CC1 (settable in the interface 'Scc')
			:return: structure: for return value, see the help for UplinkStruct structure arguments."""
		secondaryCompCarrier_cmd_val = self._base.get_repcap_cmd_value(secondaryCompCarrier, repcap.SecondaryCompCarrier)
		return self._core.io.query_struct(f'CONFigure:LTE:SIGNaling<Instance>:CONNection:SCC{secondaryCompCarrier_cmd_val}:RMC:UL?', self.__class__.UplinkStruct())

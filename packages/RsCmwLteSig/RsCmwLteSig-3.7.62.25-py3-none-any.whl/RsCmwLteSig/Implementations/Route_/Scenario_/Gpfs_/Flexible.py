from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Flexible:
	"""Flexible commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("flexible", core, parent)

	# noinspection PyTypeChecker
	class InternalStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Pcc_Bb_Board: enums.BasebandBoard: Signaling unit for the PCC
			- Pcc_Rx_Conn: enums.RxConnector: RF connector for the PCC input path
			- Pcc_Rx_Conv: enums.RxConverter: RX module for the PCC input path
			- Pcc_Tx_1_Conn: enums.TxConnector: RF connector for the first PCC output path
			- Pcc_Tx_1_Conv: enums.TxConverter: TX module for the first PCC output path
			- Pcc_Tx_2_Conn: enums.TxConnector: RF connector for the second PCC output path
			- Pcc_Tx_2_Conv: enums.TxConverter: TX module for the second PCC output path
			- Scc_1_Bb_Board: enums.BasebandBoard: Signaling unit for the SCC1
			- Scc_1_Tx_1_Conn: enums.TxConnector: RF connector for the first SCC1 output path
			- Scc_1_Tx_1_Conv: enums.TxConverter: TX module for the first SCC1 output path
			- Scc_1_Tx_2_Conn: enums.TxConnector: RF connector for the second SCC1 output path
			- Scc_1_Tx_2_Conv: enums.TxConverter: TX module for the second SCC1 output path
			- Scc_1_Tx_3_Conn: enums.TxConnector: RF connector for the third SCC1 output path
			- Scc_1_Tx_3_Conv: enums.TxConverter: TX module for the third SCC1 output path
			- Scc_1_Tx_4_Conn: enums.TxConnector: RF connector for the fourth SCC1 output path
			- Scc_1_Tx_4_Conv: enums.TxConverter: TX module for the fourth SCC1 output path
			- Scc_2_Bb_Board: enums.BasebandBoard: Signaling unit for the SCC2
			- Scc_2_Tx_1_Conn: enums.TxConnector: RF connector for the first SCC2 output path
			- Scc_2_Tx_1_Conv: enums.TxConverter: TX module for the first SCC2 output path
			- Scc_2_Tx_2_Conn: enums.TxConnector: RF connector for the second SCC2 output path
			- Scc_2_Tx_2_Conv: enums.TxConverter: TX module for the second SCC2 output path
			- Scc_3_Bb_Board: enums.BasebandBoard: Signaling unit for the SCC3
			- Scc_3_Tx_1_Conn: enums.TxConnector: RF connector for the first SCC3 output path
			- Scc_3_Tx_1_Conv: enums.TxConverter: TX module for the first SCC3 output path
			- Scc_3_Tx_2_Conn: enums.TxConnector: RF connector for the second SCC3 output path
			- Scc_3_Tx_2_Conv: enums.TxConverter: TX module for the second SCC3 output path
			- Scc_4_Bb_Board: enums.BasebandBoard: Signaling unit for the SCC4
			- Scc_4_Tx_1_Conn: enums.TxConnector: RF connector for the first SCC4 output path
			- Scc_4_Tx_1_Conv: enums.TxConverter: TX module for the first SCC4 output path
			- Scc_4_Tx_2_Conn: enums.TxConnector: RF connector for the second SCC4 output path
			- Scc_4_Tx_2_Conv: enums.TxConverter: TX module for the second SCC4 output path
			- Scc_5_Bb_Board: enums.BasebandBoard: Signaling unit for the SCC5
			- Scc_5_Tx_1_Conn: enums.TxConnector: RF connector for the first SCC5 output path
			- Scc_5_Tx_1_Conv: enums.TxConverter: TX module for the first SCC5 output path
			- Scc_5_Tx_2_Conn: enums.TxConnector: RF connector for the second SCC5 output path
			- Scc_5_Tx_2_Conv: enums.TxConverter: TX module for the second SCC5 output path
			- Scc_6_Bb_Board: enums.BasebandBoard: Signaling unit for the SCC6
			- Scc_6_Tx_1_Conn: enums.TxConnector: RF connector for the first SCC6 output path
			- Scc_6_Tx_1_Conv: enums.TxConverter: TX module for the first SCC6 output path
			- Scc_6_Tx_2_Conn: enums.TxConnector: RF connector for the second SCC6 output path
			- Scc_6_Tx_2_Conv: enums.TxConverter: TX module for the second SCC6 output path
			- Pcc_Fading_Board: enums.FadingBoard: Internal fader for the PCC
			- Scc_1_Fading_Board: enums.FadingBoard: Internal fader for the SCC1
			- Scc_2_Fading_Board: enums.FadingBoard: Internal fader for the SCC2
			- Scc_3_Fading_Board: enums.FadingBoard: Internal fader for the SCC3
			- Scc_4_Fading_Board: enums.FadingBoard: Internal fader for the SCC4
			- Scc_5_Fading_Board: enums.FadingBoard: Internal fader for the SCC5
			- Scc_6_Fading_Board: enums.FadingBoard: Internal fader for the SCC6
			- Coprocessor: enums.BasebandBoard: SUA for coprocessing"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Pcc_Bb_Board', enums.BasebandBoard),
			ArgStruct.scalar_enum('Pcc_Rx_Conn', enums.RxConnector),
			ArgStruct.scalar_enum('Pcc_Rx_Conv', enums.RxConverter),
			ArgStruct.scalar_enum('Pcc_Tx_1_Conn', enums.TxConnector),
			ArgStruct.scalar_enum('Pcc_Tx_1_Conv', enums.TxConverter),
			ArgStruct.scalar_enum('Pcc_Tx_2_Conn', enums.TxConnector),
			ArgStruct.scalar_enum('Pcc_Tx_2_Conv', enums.TxConverter),
			ArgStruct.scalar_enum('Scc_1_Bb_Board', enums.BasebandBoard),
			ArgStruct.scalar_enum('Scc_1_Tx_1_Conn', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_1_Tx_1_Conv', enums.TxConverter),
			ArgStruct.scalar_enum('Scc_1_Tx_2_Conn', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_1_Tx_2_Conv', enums.TxConverter),
			ArgStruct.scalar_enum('Scc_1_Tx_3_Conn', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_1_Tx_3_Conv', enums.TxConverter),
			ArgStruct.scalar_enum('Scc_1_Tx_4_Conn', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_1_Tx_4_Conv', enums.TxConverter),
			ArgStruct.scalar_enum('Scc_2_Bb_Board', enums.BasebandBoard),
			ArgStruct.scalar_enum('Scc_2_Tx_1_Conn', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_2_Tx_1_Conv', enums.TxConverter),
			ArgStruct.scalar_enum('Scc_2_Tx_2_Conn', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_2_Tx_2_Conv', enums.TxConverter),
			ArgStruct.scalar_enum('Scc_3_Bb_Board', enums.BasebandBoard),
			ArgStruct.scalar_enum('Scc_3_Tx_1_Conn', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_3_Tx_1_Conv', enums.TxConverter),
			ArgStruct.scalar_enum('Scc_3_Tx_2_Conn', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_3_Tx_2_Conv', enums.TxConverter),
			ArgStruct.scalar_enum('Scc_4_Bb_Board', enums.BasebandBoard),
			ArgStruct.scalar_enum('Scc_4_Tx_1_Conn', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_4_Tx_1_Conv', enums.TxConverter),
			ArgStruct.scalar_enum('Scc_4_Tx_2_Conn', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_4_Tx_2_Conv', enums.TxConverter),
			ArgStruct.scalar_enum('Scc_5_Bb_Board', enums.BasebandBoard),
			ArgStruct.scalar_enum('Scc_5_Tx_1_Conn', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_5_Tx_1_Conv', enums.TxConverter),
			ArgStruct.scalar_enum('Scc_5_Tx_2_Conn', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_5_Tx_2_Conv', enums.TxConverter),
			ArgStruct.scalar_enum('Scc_6_Bb_Board', enums.BasebandBoard),
			ArgStruct.scalar_enum('Scc_6_Tx_1_Conn', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_6_Tx_1_Conv', enums.TxConverter),
			ArgStruct.scalar_enum('Scc_6_Tx_2_Conn', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_6_Tx_2_Conv', enums.TxConverter),
			ArgStruct.scalar_enum('Pcc_Fading_Board', enums.FadingBoard),
			ArgStruct.scalar_enum('Scc_1_Fading_Board', enums.FadingBoard),
			ArgStruct.scalar_enum('Scc_2_Fading_Board', enums.FadingBoard),
			ArgStruct.scalar_enum('Scc_3_Fading_Board', enums.FadingBoard),
			ArgStruct.scalar_enum('Scc_4_Fading_Board', enums.FadingBoard),
			ArgStruct.scalar_enum('Scc_5_Fading_Board', enums.FadingBoard),
			ArgStruct.scalar_enum('Scc_6_Fading_Board', enums.FadingBoard),
			ArgStruct.scalar_enum('Coprocessor', enums.BasebandBoard)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pcc_Bb_Board: enums.BasebandBoard = None
			self.Pcc_Rx_Conn: enums.RxConnector = None
			self.Pcc_Rx_Conv: enums.RxConverter = None
			self.Pcc_Tx_1_Conn: enums.TxConnector = None
			self.Pcc_Tx_1_Conv: enums.TxConverter = None
			self.Pcc_Tx_2_Conn: enums.TxConnector = None
			self.Pcc_Tx_2_Conv: enums.TxConverter = None
			self.Scc_1_Bb_Board: enums.BasebandBoard = None
			self.Scc_1_Tx_1_Conn: enums.TxConnector = None
			self.Scc_1_Tx_1_Conv: enums.TxConverter = None
			self.Scc_1_Tx_2_Conn: enums.TxConnector = None
			self.Scc_1_Tx_2_Conv: enums.TxConverter = None
			self.Scc_1_Tx_3_Conn: enums.TxConnector = None
			self.Scc_1_Tx_3_Conv: enums.TxConverter = None
			self.Scc_1_Tx_4_Conn: enums.TxConnector = None
			self.Scc_1_Tx_4_Conv: enums.TxConverter = None
			self.Scc_2_Bb_Board: enums.BasebandBoard = None
			self.Scc_2_Tx_1_Conn: enums.TxConnector = None
			self.Scc_2_Tx_1_Conv: enums.TxConverter = None
			self.Scc_2_Tx_2_Conn: enums.TxConnector = None
			self.Scc_2_Tx_2_Conv: enums.TxConverter = None
			self.Scc_3_Bb_Board: enums.BasebandBoard = None
			self.Scc_3_Tx_1_Conn: enums.TxConnector = None
			self.Scc_3_Tx_1_Conv: enums.TxConverter = None
			self.Scc_3_Tx_2_Conn: enums.TxConnector = None
			self.Scc_3_Tx_2_Conv: enums.TxConverter = None
			self.Scc_4_Bb_Board: enums.BasebandBoard = None
			self.Scc_4_Tx_1_Conn: enums.TxConnector = None
			self.Scc_4_Tx_1_Conv: enums.TxConverter = None
			self.Scc_4_Tx_2_Conn: enums.TxConnector = None
			self.Scc_4_Tx_2_Conv: enums.TxConverter = None
			self.Scc_5_Bb_Board: enums.BasebandBoard = None
			self.Scc_5_Tx_1_Conn: enums.TxConnector = None
			self.Scc_5_Tx_1_Conv: enums.TxConverter = None
			self.Scc_5_Tx_2_Conn: enums.TxConnector = None
			self.Scc_5_Tx_2_Conv: enums.TxConverter = None
			self.Scc_6_Bb_Board: enums.BasebandBoard = None
			self.Scc_6_Tx_1_Conn: enums.TxConnector = None
			self.Scc_6_Tx_1_Conv: enums.TxConverter = None
			self.Scc_6_Tx_2_Conn: enums.TxConnector = None
			self.Scc_6_Tx_2_Conv: enums.TxConverter = None
			self.Pcc_Fading_Board: enums.FadingBoard = None
			self.Scc_1_Fading_Board: enums.FadingBoard = None
			self.Scc_2_Fading_Board: enums.FadingBoard = None
			self.Scc_3_Fading_Board: enums.FadingBoard = None
			self.Scc_4_Fading_Board: enums.FadingBoard = None
			self.Scc_5_Fading_Board: enums.FadingBoard = None
			self.Scc_6_Fading_Board: enums.FadingBoard = None
			self.Coprocessor: enums.BasebandBoard = None

	# noinspection PyTypeChecker
	def get_internal(self) -> InternalStruct:
		"""SCPI: ROUTe:LTE:SIGNaling<instance>:SCENario:GPFS<MIMO4x4>[:FLEXible]:INTernal \n
		Snippet: value: InternalStruct = driver.route.scenario.gpfs.flexible.get_internal() \n
		Activates the scenario '7CC - Fading - nx2 nx4 nx2 nx2 nx2 nx2 nx2' with internal fading and selects the signal paths.
		For possible parameter values, see 'Values for Signal Path Selection'. \n
			:return: structure: for return value, see the help for InternalStruct structure arguments.
		"""
		return self._core.io.query_struct('ROUTe:LTE:SIGNaling<Instance>:SCENario:GPFS4:FLEXible:INTernal?', self.__class__.InternalStruct())

	def set_internal(self, value: InternalStruct) -> None:
		"""SCPI: ROUTe:LTE:SIGNaling<instance>:SCENario:GPFS<MIMO4x4>[:FLEXible]:INTernal \n
		Snippet: driver.route.scenario.gpfs.flexible.set_internal(value = InternalStruct()) \n
		Activates the scenario '7CC - Fading - nx2 nx4 nx2 nx2 nx2 nx2 nx2' with internal fading and selects the signal paths.
		For possible parameter values, see 'Values for Signal Path Selection'. \n
			:param value: see the help for InternalStruct structure arguments.
		"""
		self._core.io.write_struct('ROUTe:LTE:SIGNaling<Instance>:SCENario:GPFS4:FLEXible:INTernal', value)

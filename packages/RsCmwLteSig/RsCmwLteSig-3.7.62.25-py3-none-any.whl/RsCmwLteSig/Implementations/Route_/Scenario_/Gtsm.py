from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Gtsm:
	"""Gtsm commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("gtsm", core, parent)

	# noinspection PyTypeChecker
	class FlexibleStruct(StructBase):
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
			- Scc_2_Tx_3_Conn: enums.TxConnector: RF connector for the third SCC2 output path
			- Scc_2_Tx_3_Conv: enums.TxConverter: TX module for the third SCC2 output path
			- Scc_2_Tx_4_Conn: enums.TxConnector: RF connector for the fourth SCC2 output path
			- Scc_2_Tx_4_Conv: enums.TxConverter: TX module for the fourth SCC2 output path
			- Scc_3_Bb_Board: enums.BasebandBoard: Signaling unit for the SCC3
			- Scc_3_Tx_1_Conn: enums.TxConnector: RF connector for the first SCC3 output path
			- Scc_3_Tx_1_Conv: enums.TxConverter: TX module for the first SCC3 output path
			- Scc_3_Tx_2_Conn: enums.TxConnector: RF connector for the second SCC3 output path
			- Scc_3_Tx_2_Conv: enums.TxConverter: TX module for the second SCC3 output path
			- Scc_3_Tx_3_Conn: enums.TxConnector: RF connector for the third SCC3 output path
			- Scc_3_Tx_3_Conv: enums.TxConverter: TX module for the third SCC3 output path
			- Scc_3_Tx_4_Conn: enums.TxConnector: RF connector for the fourth SCC3 output path
			- Scc_3_Tx_4_Conv: enums.TxConverter: TX module for the fourth SCC3 output path
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
			ArgStruct.scalar_enum('Scc_2_Tx_3_Conn', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_2_Tx_3_Conv', enums.TxConverter),
			ArgStruct.scalar_enum('Scc_2_Tx_4_Conn', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_2_Tx_4_Conv', enums.TxConverter),
			ArgStruct.scalar_enum('Scc_3_Bb_Board', enums.BasebandBoard),
			ArgStruct.scalar_enum('Scc_3_Tx_1_Conn', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_3_Tx_1_Conv', enums.TxConverter),
			ArgStruct.scalar_enum('Scc_3_Tx_2_Conn', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_3_Tx_2_Conv', enums.TxConverter),
			ArgStruct.scalar_enum('Scc_3_Tx_3_Conn', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_3_Tx_3_Conv', enums.TxConverter),
			ArgStruct.scalar_enum('Scc_3_Tx_4_Conn', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_3_Tx_4_Conv', enums.TxConverter),
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
			self.Scc_2_Tx_3_Conn: enums.TxConnector = None
			self.Scc_2_Tx_3_Conv: enums.TxConverter = None
			self.Scc_2_Tx_4_Conn: enums.TxConnector = None
			self.Scc_2_Tx_4_Conv: enums.TxConverter = None
			self.Scc_3_Bb_Board: enums.BasebandBoard = None
			self.Scc_3_Tx_1_Conn: enums.TxConnector = None
			self.Scc_3_Tx_1_Conv: enums.TxConverter = None
			self.Scc_3_Tx_2_Conn: enums.TxConnector = None
			self.Scc_3_Tx_2_Conv: enums.TxConverter = None
			self.Scc_3_Tx_3_Conn: enums.TxConnector = None
			self.Scc_3_Tx_3_Conv: enums.TxConverter = None
			self.Scc_3_Tx_4_Conn: enums.TxConnector = None
			self.Scc_3_Tx_4_Conv: enums.TxConverter = None
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
			self.Coprocessor: enums.BasebandBoard = None

	# noinspection PyTypeChecker
	def get_flexible(self) -> FlexibleStruct:
		"""SCPI: ROUTe:LTE:SIGNaling<instance>:SCENario:GTSM<Mimo4x4>[:FLEXible] \n
		Snippet: value: FlexibleStruct = driver.route.scenario.gtsm.get_flexible() \n
		Activates the scenario '7CC - nx2 nx4 nx4 nx4 nx2 nx2 nx2' and selects the signal paths. For possible parameter values,
		see 'Values for Signal Path Selection'. \n
			:return: structure: for return value, see the help for FlexibleStruct structure arguments.
		"""
		return self._core.io.query_struct('ROUTe:LTE:SIGNaling<Instance>:SCENario:GTSM4:FLEXible?', self.__class__.FlexibleStruct())

	def set_flexible(self, value: FlexibleStruct) -> None:
		"""SCPI: ROUTe:LTE:SIGNaling<instance>:SCENario:GTSM<Mimo4x4>[:FLEXible] \n
		Snippet: driver.route.scenario.gtsm.set_flexible(value = FlexibleStruct()) \n
		Activates the scenario '7CC - nx2 nx4 nx4 nx4 nx2 nx2 nx2' and selects the signal paths. For possible parameter values,
		see 'Values for Signal Path Selection'. \n
			:param value: see the help for FlexibleStruct structure arguments.
		"""
		self._core.io.write_struct('ROUTe:LTE:SIGNaling<Instance>:SCENario:GTSM4:FLEXible', value)

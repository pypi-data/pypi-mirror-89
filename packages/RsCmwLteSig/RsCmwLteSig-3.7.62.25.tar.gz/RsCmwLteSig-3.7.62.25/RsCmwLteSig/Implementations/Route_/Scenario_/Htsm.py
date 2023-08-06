from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Htsm:
	"""Htsm commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("htsm", core, parent)

	# noinspection PyTypeChecker
	class FlexibleStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Pcc_Bb_Board: enums.BasebandBoard: No parameter help available
			- Pcc_Rx_Conn: enums.RxConnector: No parameter help available
			- Pcc_Rx_Conv: enums.RxConverter: No parameter help available
			- Pcc_Tx_1_Conn: enums.TxConnector: No parameter help available
			- Pcc_Tx_1_Conv: enums.TxConverter: No parameter help available
			- Pcc_Tx_2_Conn: enums.TxConnector: No parameter help available
			- Pcc_Tx_2_Conv: enums.TxConverter: No parameter help available
			- Scc_1_Bb_Board: enums.BasebandBoard: No parameter help available
			- Scc_1_Tx_1_Conn: enums.TxConnector: No parameter help available
			- Scc_1_Tx_1_Conv: enums.TxConverter: No parameter help available
			- Scc_1_Tx_2_Conn: enums.TxConnector: No parameter help available
			- Scc_1_Tx_2_Conv: enums.TxConverter: No parameter help available
			- Scc_1_Tx_3_Conn: enums.TxConnector: No parameter help available
			- Scc_1_Tx_3_Conv: enums.TxConverter: No parameter help available
			- Scc_1_Tx_4_Conn: enums.TxConnector: No parameter help available
			- Scc_1_Tx_4_Conv: enums.TxConverter: No parameter help available
			- Scc_2_Bb_Board: enums.BasebandBoard: No parameter help available
			- Scc_2_Tx_1_Conn: enums.TxConnector: No parameter help available
			- Scc_2_Tx_1_Conv: enums.TxConverter: No parameter help available
			- Scc_2_Tx_2_Conn: enums.TxConnector: No parameter help available
			- Scc_2_Tx_2_Conv: enums.TxConverter: No parameter help available
			- Scc_2_Tx_3_Conn: enums.TxConnector: No parameter help available
			- Scc_2_Tx_3_Conv: enums.TxConverter: No parameter help available
			- Scc_2_Tx_4_Conn: enums.TxConnector: No parameter help available
			- Scc_2_Tx_4_Conv: enums.TxConverter: No parameter help available
			- Scc_3_Bb_Board: enums.BasebandBoard: No parameter help available
			- Scc_3_Tx_1_Conn: enums.TxConnector: No parameter help available
			- Scc_3_Tx_1_Conv: enums.TxConverter: No parameter help available
			- Scc_3_Tx_2_Conn: enums.TxConnector: No parameter help available
			- Scc_3_Tx_2_Conv: enums.TxConverter: No parameter help available
			- Scc_4_Bb_Board: enums.BasebandBoard: No parameter help available
			- Scc_4_Tx_1_Conn: enums.TxConnector: No parameter help available
			- Scc_4_Tx_1_Conv: enums.TxConverter: No parameter help available
			- Scc_4_Tx_2_Conn: enums.TxConnector: No parameter help available
			- Scc_4_Tx_2_Conv: enums.TxConverter: No parameter help available
			- Scc_5_Bb_Board: enums.BasebandBoard: No parameter help available
			- Scc_5_Tx_1_Conn: enums.TxConnector: No parameter help available
			- Scc_5_Tx_1_Conv: enums.TxConverter: No parameter help available
			- Scc_5_Tx_2_Conn: enums.TxConnector: No parameter help available
			- Scc_5_Tx_2_Conv: enums.TxConverter: No parameter help available
			- Scc_6_Bb_Board: enums.BasebandBoard: No parameter help available
			- Scc_6_Tx_1_Conn: enums.TxConnector: No parameter help available
			- Scc_6_Tx_1_Conv: enums.TxConverter: No parameter help available
			- Scc_6_Tx_2_Conn: enums.TxConnector: No parameter help available
			- Scc_6_Tx_2_Conv: enums.TxConverter: No parameter help available
			- Scc_7_Bb_Board: enums.BasebandBoard: No parameter help available
			- Scc_7_Tx_1_Conn: enums.TxConnector: No parameter help available
			- Scc_7_Tx_1_Conv: enums.TxConverter: No parameter help available
			- Scc_7_Tx_2_Conn: enums.TxConnector: No parameter help available
			- Scc_7_Tx_2_Conv: enums.TxConverter: No parameter help available
			- Coprocessor: enums.BasebandBoard: No parameter help available"""
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
			ArgStruct.scalar_enum('Scc_7_Bb_Board', enums.BasebandBoard),
			ArgStruct.scalar_enum('Scc_7_Tx_1_Conn', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_7_Tx_1_Conv', enums.TxConverter),
			ArgStruct.scalar_enum('Scc_7_Tx_2_Conn', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_7_Tx_2_Conv', enums.TxConverter),
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
			self.Scc_7_Bb_Board: enums.BasebandBoard = None
			self.Scc_7_Tx_1_Conn: enums.TxConnector = None
			self.Scc_7_Tx_1_Conv: enums.TxConverter = None
			self.Scc_7_Tx_2_Conn: enums.TxConnector = None
			self.Scc_7_Tx_2_Conv: enums.TxConverter = None
			self.Coprocessor: enums.BasebandBoard = None

	# noinspection PyTypeChecker
	def get_flexible(self) -> FlexibleStruct:
		"""SCPI: ROUTe:LTE:SIGNaling<instance>:SCENario:HTSM<MIMO4x4>[:FLEXible] \n
		Snippet: value: FlexibleStruct = driver.route.scenario.htsm.get_flexible() \n
		No command help available \n
			:return: structure: for return value, see the help for FlexibleStruct structure arguments.
		"""
		return self._core.io.query_struct('ROUTe:LTE:SIGNaling<Instance>:SCENario:HTSM4:FLEXible?', self.__class__.FlexibleStruct())

	def set_flexible(self, value: FlexibleStruct) -> None:
		"""SCPI: ROUTe:LTE:SIGNaling<instance>:SCENario:HTSM<MIMO4x4>[:FLEXible] \n
		Snippet: driver.route.scenario.htsm.set_flexible(value = FlexibleStruct()) \n
		No command help available \n
			:param value: see the help for FlexibleStruct structure arguments.
		"""
		self._core.io.write_struct('ROUTe:LTE:SIGNaling<Instance>:SCENario:HTSM4:FLEXible', value)

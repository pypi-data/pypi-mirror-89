from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dd:
	"""Dd commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dd", core, parent)

	# noinspection PyTypeChecker
	class FlexibleStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Pcc_Bb_Board: enums.BasebandBoard: Signaling unit for the PCC
			- Rx_Connector: enums.RxConnector: RF connector for the PCC input path
			- Rx_Converter: enums.RxConverter: RX module for the PCC input path
			- Tx_1_Connector: enums.TxConnector: RF connector for the PCC output path
			- Tx_1_Converter: enums.TxConverter: TX module for the PCC output path
			- Scc_1_Bb_Board: enums.BasebandBoard: Signaling unit for the SCC1
			- Tx_2_Connector: enums.TxConnector: RF connector for the SCC1 output path
			- Tx_2_Converter: enums.TxConverter: TX module for the SCC1 output path
			- Scc_Bb_Board_2: enums.BasebandBoard: Signaling unit for the SCC2
			- Tx_3_Connector: enums.TxConnector: RF connector for the SCC2 output path
			- Tx_3_Converter: enums.TxConverter: TX module for the SCC2 output path
			- Scc_Bb_Board_3: enums.BasebandBoard: Signaling unit for the SCC3
			- Tx_4_Connector: enums.TxConnector: RF connector for the SCC3 output path
			- Tx_4_Converter: enums.TxConverter: TX module for the SCC3 output path
			- Coprocessor: enums.BasebandBoard: SUA for coprocessing"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Pcc_Bb_Board', enums.BasebandBoard),
			ArgStruct.scalar_enum('Rx_Connector', enums.RxConnector),
			ArgStruct.scalar_enum('Rx_Converter', enums.RxConverter),
			ArgStruct.scalar_enum('Tx_1_Connector', enums.TxConnector),
			ArgStruct.scalar_enum('Tx_1_Converter', enums.TxConverter),
			ArgStruct.scalar_enum('Scc_1_Bb_Board', enums.BasebandBoard),
			ArgStruct.scalar_enum('Tx_2_Connector', enums.TxConnector),
			ArgStruct.scalar_enum('Tx_2_Converter', enums.TxConverter),
			ArgStruct.scalar_enum('Scc_Bb_Board_2', enums.BasebandBoard),
			ArgStruct.scalar_enum('Tx_3_Connector', enums.TxConnector),
			ArgStruct.scalar_enum('Tx_3_Converter', enums.TxConverter),
			ArgStruct.scalar_enum('Scc_Bb_Board_3', enums.BasebandBoard),
			ArgStruct.scalar_enum('Tx_4_Connector', enums.TxConnector),
			ArgStruct.scalar_enum('Tx_4_Converter', enums.TxConverter),
			ArgStruct.scalar_enum('Coprocessor', enums.BasebandBoard)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pcc_Bb_Board: enums.BasebandBoard = None
			self.Rx_Connector: enums.RxConnector = None
			self.Rx_Converter: enums.RxConverter = None
			self.Tx_1_Connector: enums.TxConnector = None
			self.Tx_1_Converter: enums.TxConverter = None
			self.Scc_1_Bb_Board: enums.BasebandBoard = None
			self.Tx_2_Connector: enums.TxConnector = None
			self.Tx_2_Converter: enums.TxConverter = None
			self.Scc_Bb_Board_2: enums.BasebandBoard = None
			self.Tx_3_Connector: enums.TxConnector = None
			self.Tx_3_Converter: enums.TxConverter = None
			self.Scc_Bb_Board_3: enums.BasebandBoard = None
			self.Tx_4_Connector: enums.TxConnector = None
			self.Tx_4_Converter: enums.TxConverter = None
			self.Coprocessor: enums.BasebandBoard = None

	# noinspection PyTypeChecker
	def get_flexible(self) -> FlexibleStruct:
		"""SCPI: ROUTe:LTE:SIGNaling<instance>:SCENario:DD:FLEXible \n
		Snippet: value: FlexibleStruct = driver.route.scenario.dd.get_flexible() \n
		Activates the scenario '4CC - 1x1 1x1 1x1 1x1' and selects the signal paths. For possible parameter values, see 'Values
		for Signal Path Selection'. \n
			:return: structure: for return value, see the help for FlexibleStruct structure arguments.
		"""
		return self._core.io.query_struct('ROUTe:LTE:SIGNaling<Instance>:SCENario:DD:FLEXible?', self.__class__.FlexibleStruct())

	def set_flexible(self, value: FlexibleStruct) -> None:
		"""SCPI: ROUTe:LTE:SIGNaling<instance>:SCENario:DD:FLEXible \n
		Snippet: driver.route.scenario.dd.set_flexible(value = FlexibleStruct()) \n
		Activates the scenario '4CC - 1x1 1x1 1x1 1x1' and selects the signal paths. For possible parameter values, see 'Values
		for Signal Path Selection'. \n
			:param value: see the help for FlexibleStruct structure arguments.
		"""
		self._core.io.write_struct('ROUTe:LTE:SIGNaling<Instance>:SCENario:DD:FLEXible', value)

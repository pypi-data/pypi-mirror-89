from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ccms:
	"""Ccms commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ccms", core, parent)

	# noinspection PyTypeChecker
	class FlexibleStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Pcc_Bb_Board: enums.BasebandBoard: Signaling unit for the PCC
			- Rx_Connector: enums.RxConnector: RF connector for the PCC input path
			- Rx_Converter: enums.RxConverter: RX module for the PCC input path
			- Pcc_Tx_1_Connector: enums.TxConnector: RF connector for the PCC output path
			- Pcc_Tx_1_Converter: enums.TxConverter: TX module for the PCC output path
			- Scc_1_Bb_Board: enums.BasebandBoard: Signaling unit for the SCC1
			- Scc_1_Tx_1_Connect: enums.TxConnector: RF connector for the first SCC1 output path
			- Scc_1_Tx_1_Convert: enums.TxConverter: TX module for the first SCC1 output path
			- Scc_1_Tx_2_Connect: enums.TxConnector: RF connector for the second SCC1 output path
			- Scc_1_Tx_2_Convert: enums.TxConverter: TX module for the second SCC1 output path
			- Scc_2_Bb_Board: enums.BasebandBoard: Signaling unit for the SCC2
			- Scc_2_Tx_Connector: enums.TxConnector: RF connector for the SCC2 output path
			- Scc_2_Tx_Converter: enums.TxConverter: TX module for the SCC2 output path"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Pcc_Bb_Board', enums.BasebandBoard),
			ArgStruct.scalar_enum('Rx_Connector', enums.RxConnector),
			ArgStruct.scalar_enum('Rx_Converter', enums.RxConverter),
			ArgStruct.scalar_enum('Pcc_Tx_1_Connector', enums.TxConnector),
			ArgStruct.scalar_enum('Pcc_Tx_1_Converter', enums.TxConverter),
			ArgStruct.scalar_enum('Scc_1_Bb_Board', enums.BasebandBoard),
			ArgStruct.scalar_enum('Scc_1_Tx_1_Connect', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_1_Tx_1_Convert', enums.TxConverter),
			ArgStruct.scalar_enum('Scc_1_Tx_2_Connect', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_1_Tx_2_Convert', enums.TxConverter),
			ArgStruct.scalar_enum('Scc_2_Bb_Board', enums.BasebandBoard),
			ArgStruct.scalar_enum('Scc_2_Tx_Connector', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_2_Tx_Converter', enums.TxConverter)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pcc_Bb_Board: enums.BasebandBoard = None
			self.Rx_Connector: enums.RxConnector = None
			self.Rx_Converter: enums.RxConverter = None
			self.Pcc_Tx_1_Connector: enums.TxConnector = None
			self.Pcc_Tx_1_Converter: enums.TxConverter = None
			self.Scc_1_Bb_Board: enums.BasebandBoard = None
			self.Scc_1_Tx_1_Connect: enums.TxConnector = None
			self.Scc_1_Tx_1_Convert: enums.TxConverter = None
			self.Scc_1_Tx_2_Connect: enums.TxConnector = None
			self.Scc_1_Tx_2_Convert: enums.TxConverter = None
			self.Scc_2_Bb_Board: enums.BasebandBoard = None
			self.Scc_2_Tx_Connector: enums.TxConnector = None
			self.Scc_2_Tx_Converter: enums.TxConverter = None

	# noinspection PyTypeChecker
	def get_flexible(self) -> FlexibleStruct:
		"""SCPI: ROUTe:LTE:SIGNaling<instance>:SCENario:CCMS<Carrier>:FLEXible \n
		Snippet: value: FlexibleStruct = driver.route.scenario.ccms.get_flexible() \n
		Activates the scenario '3CC - 1x1 nx2 1x1' and selects the signal paths. For possible parameter values, see 'Values for
		Signal Path Selection'. \n
			:return: structure: for return value, see the help for FlexibleStruct structure arguments.
		"""
		return self._core.io.query_struct('ROUTe:LTE:SIGNaling<Instance>:SCENario:CCMS1:FLEXible?', self.__class__.FlexibleStruct())

	def set_flexible(self, value: FlexibleStruct) -> None:
		"""SCPI: ROUTe:LTE:SIGNaling<instance>:SCENario:CCMS<Carrier>:FLEXible \n
		Snippet: driver.route.scenario.ccms.set_flexible(value = FlexibleStruct()) \n
		Activates the scenario '3CC - 1x1 nx2 1x1' and selects the signal paths. For possible parameter values, see 'Values for
		Signal Path Selection'. \n
			:param value: see the help for FlexibleStruct structure arguments.
		"""
		self._core.io.write_struct('ROUTe:LTE:SIGNaling<Instance>:SCENario:CCMS1:FLEXible', value)

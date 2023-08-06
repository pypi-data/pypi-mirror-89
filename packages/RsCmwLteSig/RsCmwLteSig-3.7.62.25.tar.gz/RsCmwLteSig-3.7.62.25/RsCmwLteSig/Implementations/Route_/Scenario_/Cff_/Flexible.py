from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Flexible:
	"""Flexible commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("flexible", core, parent)

	# noinspection PyTypeChecker
	class ExternalStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Pcc_Bb_Board: enums.BasebandBoard: No parameter help available
			- Rx_Connector: enums.RxConnector: No parameter help available
			- Rx_Converter: enums.RxConverter: No parameter help available
			- Pcc_Tx_1_Connector: enums.TxConnector: No parameter help available
			- Pcc_Tx_1_Converter: enums.TxConverter: No parameter help available
			- Pcc_Iq_1_Connector: enums.TxConnector: No parameter help available
			- Pcc_Tx_2_Connector: enums.TxConnector: No parameter help available
			- Pcc_Tx_2_Converter: enums.TxConverter: No parameter help available
			- Pcc_Iq_2_Connector: enums.TxConnector: No parameter help available
			- Scc_1_Bb_Board: enums.BasebandBoard: No parameter help available
			- Scc_1_Tx_1_Conn: enums.TxConnector: No parameter help available
			- Scc_1_Tx_1_Conv: enums.TxConverter: No parameter help available
			- Scc_1_Iq_1_Conn: enums.TxConnector: No parameter help available
			- Scc_1_Tx_2_Conn: enums.TxConnector: No parameter help available
			- Scc_1_Tx_2_Conv: enums.TxConverter: No parameter help available
			- Scc_1_Iq_2_Conn: enums.TxConnector: No parameter help available
			- Scc_2_Bb_Board: enums.BasebandBoard: No parameter help available
			- Scc_2_Tx_1_Conn: enums.TxConnector: No parameter help available
			- Scc_2_Tx_1_Conv: enums.TxConverter: No parameter help available
			- Scc_2_Iq_1_Conn: enums.TxConnector: No parameter help available
			- Scc_2_Tx_2_Conn: enums.TxConnector: No parameter help available
			- Scc_2_Tx_2_Conv: enums.TxConverter: No parameter help available
			- Scc_2_Iq_2_Conn: enums.TxConnector: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Pcc_Bb_Board', enums.BasebandBoard),
			ArgStruct.scalar_enum('Rx_Connector', enums.RxConnector),
			ArgStruct.scalar_enum('Rx_Converter', enums.RxConverter),
			ArgStruct.scalar_enum('Pcc_Tx_1_Connector', enums.TxConnector),
			ArgStruct.scalar_enum('Pcc_Tx_1_Converter', enums.TxConverter),
			ArgStruct.scalar_enum('Pcc_Iq_1_Connector', enums.TxConnector),
			ArgStruct.scalar_enum('Pcc_Tx_2_Connector', enums.TxConnector),
			ArgStruct.scalar_enum('Pcc_Tx_2_Converter', enums.TxConverter),
			ArgStruct.scalar_enum('Pcc_Iq_2_Connector', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_1_Bb_Board', enums.BasebandBoard),
			ArgStruct.scalar_enum('Scc_1_Tx_1_Conn', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_1_Tx_1_Conv', enums.TxConverter),
			ArgStruct.scalar_enum('Scc_1_Iq_1_Conn', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_1_Tx_2_Conn', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_1_Tx_2_Conv', enums.TxConverter),
			ArgStruct.scalar_enum('Scc_1_Iq_2_Conn', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_2_Bb_Board', enums.BasebandBoard),
			ArgStruct.scalar_enum('Scc_2_Tx_1_Conn', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_2_Tx_1_Conv', enums.TxConverter),
			ArgStruct.scalar_enum('Scc_2_Iq_1_Conn', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_2_Tx_2_Conn', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_2_Tx_2_Conv', enums.TxConverter),
			ArgStruct.scalar_enum('Scc_2_Iq_2_Conn', enums.TxConnector)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pcc_Bb_Board: enums.BasebandBoard = None
			self.Rx_Connector: enums.RxConnector = None
			self.Rx_Converter: enums.RxConverter = None
			self.Pcc_Tx_1_Connector: enums.TxConnector = None
			self.Pcc_Tx_1_Converter: enums.TxConverter = None
			self.Pcc_Iq_1_Connector: enums.TxConnector = None
			self.Pcc_Tx_2_Connector: enums.TxConnector = None
			self.Pcc_Tx_2_Converter: enums.TxConverter = None
			self.Pcc_Iq_2_Connector: enums.TxConnector = None
			self.Scc_1_Bb_Board: enums.BasebandBoard = None
			self.Scc_1_Tx_1_Conn: enums.TxConnector = None
			self.Scc_1_Tx_1_Conv: enums.TxConverter = None
			self.Scc_1_Iq_1_Conn: enums.TxConnector = None
			self.Scc_1_Tx_2_Conn: enums.TxConnector = None
			self.Scc_1_Tx_2_Conv: enums.TxConverter = None
			self.Scc_1_Iq_2_Conn: enums.TxConnector = None
			self.Scc_2_Bb_Board: enums.BasebandBoard = None
			self.Scc_2_Tx_1_Conn: enums.TxConnector = None
			self.Scc_2_Tx_1_Conv: enums.TxConverter = None
			self.Scc_2_Iq_1_Conn: enums.TxConnector = None
			self.Scc_2_Tx_2_Conn: enums.TxConnector = None
			self.Scc_2_Tx_2_Conv: enums.TxConverter = None
			self.Scc_2_Iq_2_Conn: enums.TxConnector = None

	# noinspection PyTypeChecker
	def get_external(self) -> ExternalStruct:
		"""SCPI: ROUTe:LTE:SIGNaling<instance>:SCENario:CFF[:FLEXible][:EXTernal] \n
		Snippet: value: ExternalStruct = driver.route.scenario.cff.flexible.get_external() \n
		No command help available \n
			:return: structure: for return value, see the help for ExternalStruct structure arguments.
		"""
		return self._core.io.query_struct('ROUTe:LTE:SIGNaling<Instance>:SCENario:CFF:FLEXible:EXTernal?', self.__class__.ExternalStruct())

	def set_external(self, value: ExternalStruct) -> None:
		"""SCPI: ROUTe:LTE:SIGNaling<instance>:SCENario:CFF[:FLEXible][:EXTernal] \n
		Snippet: driver.route.scenario.cff.flexible.set_external(value = ExternalStruct()) \n
		No command help available \n
			:param value: see the help for ExternalStruct structure arguments.
		"""
		self._core.io.write_struct('ROUTe:LTE:SIGNaling<Instance>:SCENario:CFF:FLEXible:EXTernal', value)

	# noinspection PyTypeChecker
	class InternalStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Pcc_Bb_Board: enums.BasebandBoard: Signaling unit for the PCC
			- Rx_Connector: enums.RxConnector: RF connector for the PCC input path
			- Rx_Converter: enums.RxConverter: RX module for the PCC input path
			- Pcc_Tx_1_Connector: enums.TxConnector: RF connector for the first PCC output path
			- Pcc_Tx_1_Converter: enums.TxConverter: TX module for the first PCC output path
			- Pcc_Tx_2_Connector: enums.TxConnector: RF connector for the second PCC output path
			- Pcc_Tx_2_Converter: enums.TxConverter: TX module for the second PCC output path
			- Scc_1_Bb_Board: enums.BasebandBoard: Signaling unit for the SCC1
			- Scc_1_Tx_1_Connector: enums.TxConnector: RF connector for the first SCC1 output path
			- Scc_1_Tx_1_Converter: enums.TxConverter: TX module for the first SCC1 output path
			- Scc_1_Tx_2_Connector: enums.TxConnector: RF connector for the second SCC1 output path
			- Scc_1_Tx_2_Converter: enums.TxConverter: TX module for the second SCC1 output path
			- Scc_2_Bb_Board: enums.BasebandBoard: Signaling unit for the SCC2
			- Scc_2_Tx_1_Connector: enums.TxConnector: RF connector for the first SCC2 output path
			- Scc_2_Tx_1_Converter: enums.TxConverter: TX module for the first SCC2 output path
			- Scc_2_Tx_2_Connector: enums.TxConnector: RF connector for the second SCC2 output path
			- Scc_2_Tx_2_Converter: enums.TxConverter: TX module for the second SCC2 output path
			- Pcc_Fading_Board: enums.FadingBoard: Internal fader for the PCC
			- Scc_1_Fading_Board: enums.FadingBoard: Internal fader for the SCC1
			- Scc_2_Fading_Board: enums.FadingBoard: Internal fader for the SCC2
			- Coprocessor: enums.BasebandBoard: SUA for coprocessing"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Pcc_Bb_Board', enums.BasebandBoard),
			ArgStruct.scalar_enum('Rx_Connector', enums.RxConnector),
			ArgStruct.scalar_enum('Rx_Converter', enums.RxConverter),
			ArgStruct.scalar_enum('Pcc_Tx_1_Connector', enums.TxConnector),
			ArgStruct.scalar_enum('Pcc_Tx_1_Converter', enums.TxConverter),
			ArgStruct.scalar_enum('Pcc_Tx_2_Connector', enums.TxConnector),
			ArgStruct.scalar_enum('Pcc_Tx_2_Converter', enums.TxConverter),
			ArgStruct.scalar_enum('Scc_1_Bb_Board', enums.BasebandBoard),
			ArgStruct.scalar_enum('Scc_1_Tx_1_Connector', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_1_Tx_1_Converter', enums.TxConverter),
			ArgStruct.scalar_enum('Scc_1_Tx_2_Connector', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_1_Tx_2_Converter', enums.TxConverter),
			ArgStruct.scalar_enum('Scc_2_Bb_Board', enums.BasebandBoard),
			ArgStruct.scalar_enum('Scc_2_Tx_1_Connector', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_2_Tx_1_Converter', enums.TxConverter),
			ArgStruct.scalar_enum('Scc_2_Tx_2_Connector', enums.TxConnector),
			ArgStruct.scalar_enum('Scc_2_Tx_2_Converter', enums.TxConverter),
			ArgStruct.scalar_enum('Pcc_Fading_Board', enums.FadingBoard),
			ArgStruct.scalar_enum('Scc_1_Fading_Board', enums.FadingBoard),
			ArgStruct.scalar_enum('Scc_2_Fading_Board', enums.FadingBoard),
			ArgStruct.scalar_enum('Coprocessor', enums.BasebandBoard)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pcc_Bb_Board: enums.BasebandBoard = None
			self.Rx_Connector: enums.RxConnector = None
			self.Rx_Converter: enums.RxConverter = None
			self.Pcc_Tx_1_Connector: enums.TxConnector = None
			self.Pcc_Tx_1_Converter: enums.TxConverter = None
			self.Pcc_Tx_2_Connector: enums.TxConnector = None
			self.Pcc_Tx_2_Converter: enums.TxConverter = None
			self.Scc_1_Bb_Board: enums.BasebandBoard = None
			self.Scc_1_Tx_1_Connector: enums.TxConnector = None
			self.Scc_1_Tx_1_Converter: enums.TxConverter = None
			self.Scc_1_Tx_2_Connector: enums.TxConnector = None
			self.Scc_1_Tx_2_Converter: enums.TxConverter = None
			self.Scc_2_Bb_Board: enums.BasebandBoard = None
			self.Scc_2_Tx_1_Connector: enums.TxConnector = None
			self.Scc_2_Tx_1_Converter: enums.TxConverter = None
			self.Scc_2_Tx_2_Connector: enums.TxConnector = None
			self.Scc_2_Tx_2_Converter: enums.TxConverter = None
			self.Pcc_Fading_Board: enums.FadingBoard = None
			self.Scc_1_Fading_Board: enums.FadingBoard = None
			self.Scc_2_Fading_Board: enums.FadingBoard = None
			self.Coprocessor: enums.BasebandBoard = None

	# noinspection PyTypeChecker
	def get_internal(self) -> InternalStruct:
		"""SCPI: ROUTe:LTE:SIGNaling<instance>:SCENario:CFF[:FLEXible]:INTernal \n
		Snippet: value: InternalStruct = driver.route.scenario.cff.flexible.get_internal() \n
		Activates the scenario '3CC - Fading - nx2 nx2 nx2' with internal fading and selects the signal paths. For possible
		parameter values, see 'Values for Signal Path Selection'. \n
			:return: structure: for return value, see the help for InternalStruct structure arguments.
		"""
		return self._core.io.query_struct('ROUTe:LTE:SIGNaling<Instance>:SCENario:CFF:FLEXible:INTernal?', self.__class__.InternalStruct())

	def set_internal(self, value: InternalStruct) -> None:
		"""SCPI: ROUTe:LTE:SIGNaling<instance>:SCENario:CFF[:FLEXible]:INTernal \n
		Snippet: driver.route.scenario.cff.flexible.set_internal(value = InternalStruct()) \n
		Activates the scenario '3CC - Fading - nx2 nx2 nx2' with internal fading and selects the signal paths. For possible
		parameter values, see 'Values for Signal Path Selection'. \n
			:param value: see the help for InternalStruct structure arguments.
		"""
		self._core.io.write_struct('ROUTe:LTE:SIGNaling<Instance>:SCENario:CFF:FLEXible:INTernal', value)

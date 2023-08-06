from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Line:
	"""Line commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: MatrixLine, default value after init: MatrixLine.Line1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("line", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_matrixLine_get', 'repcap_matrixLine_set', repcap.MatrixLine.Line1)

	def repcap_matrixLine_set(self, enum_value: repcap.MatrixLine) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to MatrixLine.Default
		Default value after init: MatrixLine.Line1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_matrixLine_get(self) -> repcap.MatrixLine:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	# noinspection PyTypeChecker
	class SetStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- H_1_Xabs: float: Range: 0 to 1
			- H_1_Xphi: int: Range: 0 deg to 345 deg, Unit: deg
			- H_2_Xabs: float: Range: 0 to 1
			- H_2_Xphi: int: Range: 0 deg to 345 deg, Unit: deg
			- H_3_Xabs: float: Range: 0 to 1
			- H_3_Xphi: int: Range: 0 deg to 345 deg, Unit: deg
			- H_4_Xphi: int: Range: 0 deg to 345 deg, Unit: deg"""
		__meta_args_list = [
			ArgStruct.scalar_float('H_1_Xabs'),
			ArgStruct.scalar_int('H_1_Xphi'),
			ArgStruct.scalar_float('H_2_Xabs'),
			ArgStruct.scalar_int('H_2_Xphi'),
			ArgStruct.scalar_float('H_3_Xabs'),
			ArgStruct.scalar_int('H_3_Xphi'),
			ArgStruct.scalar_float('H_4_Xabs'),
			ArgStruct.scalar_int('H_4_Xphi')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.H_1_Xabs: float = None
			self.H_1_Xphi: int = None
			self.H_2_Xabs: float = None
			self.H_2_Xphi: int = None
			self.H_3_Xabs: float = None
			self.H_3_Xphi: int = None
			self.H_4_Xphi: int = None

	def set(self, structure: SetStruct, matrixLine=repcap.MatrixLine.Default) -> None:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:CONNection[:PCC]:TM<nr>:CMATrix:MIMO<Mimo>:LINE<line> \n
		Snippet: driver.configure.connection.pcc.tm.cmatrix.mimo.line.set(value = [PROPERTY_STRUCT_NAME](), matrixLine = repcap.MatrixLine.Default) \n
		Configures the coefficients of the user-defined 4x4 channel matrix for TM 9.
			INTRO_CMD_HELP: There are two types of parameters: \n
			- <hnmabs> defines the square of the magnitude of the channel coefficient nm: <hnmabs> = (hnm) 2 The sum of all values in one matrix line must not be greater than 1. <h4xabs> is calculated automatically, so that the sum equals 1.
			- <hnmphi> defines the phase of the channel coefficient nm: <hnmphi> = φ(hnm)
		A query returns <h1xabs>, <h1xphi>, <h2xabs>, ..., <h4xabs>, <h4xphi>. \n
			:param structure: for set value, see the help for SetStruct structure arguments.
			:param matrixLine: optional repeated capability selector. Default value: Line1 (settable in the interface 'Line')"""
		matrixLine_cmd_val = self._base.get_repcap_cmd_value(matrixLine, repcap.MatrixLine)
		self._core.io.write_struct(f'CONFigure:LTE:SIGNaling<Instance>:CONNection:PCC:TM9:CMATrix:MIMO44:LINE{matrixLine_cmd_val}', structure)

	# noinspection PyTypeChecker
	class GetStruct(StructBase):
		"""Response structure. Fields: \n
			- H_1_Xabs: float: Range: 0 to 1
			- H_1_Xphi: int: Range: 0 deg to 345 deg, Unit: deg
			- H_2_Xabs: float: Range: 0 to 1
			- H_2_Xphi: int: Range: 0 deg to 345 deg, Unit: deg
			- H_3_Xabs: float: Range: 0 to 1
			- H_3_Xphi: int: Range: 0 deg to 345 deg, Unit: deg
			- H_4_Xabs: float: Range: 0 to 1
			- H_4_Xphi: int: Range: 0 deg to 345 deg, Unit: deg"""
		__meta_args_list = [
			ArgStruct.scalar_float('H_1_Xabs'),
			ArgStruct.scalar_int('H_1_Xphi'),
			ArgStruct.scalar_float('H_2_Xabs'),
			ArgStruct.scalar_int('H_2_Xphi'),
			ArgStruct.scalar_float('H_3_Xabs'),
			ArgStruct.scalar_int('H_3_Xphi'),
			ArgStruct.scalar_float('H_4_Xabs'),
			ArgStruct.scalar_int('H_4_Xphi')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.H_1_Xabs: float = None
			self.H_1_Xphi: int = None
			self.H_2_Xabs: float = None
			self.H_2_Xphi: int = None
			self.H_3_Xabs: float = None
			self.H_3_Xphi: int = None
			self.H_4_Xabs: float = None
			self.H_4_Xphi: int = None

	def get(self, matrixLine=repcap.MatrixLine.Default) -> GetStruct:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:CONNection[:PCC]:TM<nr>:CMATrix:MIMO<Mimo>:LINE<line> \n
		Snippet: value: GetStruct = driver.configure.connection.pcc.tm.cmatrix.mimo.line.get(matrixLine = repcap.MatrixLine.Default) \n
		Configures the coefficients of the user-defined 4x4 channel matrix for TM 9.
			INTRO_CMD_HELP: There are two types of parameters: \n
			- <hnmabs> defines the square of the magnitude of the channel coefficient nm: <hnmabs> = (hnm) 2 The sum of all values in one matrix line must not be greater than 1. <h4xabs> is calculated automatically, so that the sum equals 1.
			- <hnmphi> defines the phase of the channel coefficient nm: <hnmphi> = φ(hnm)
		A query returns <h1xabs>, <h1xphi>, <h2xabs>, ..., <h4xabs>, <h4xphi>. \n
			:param matrixLine: optional repeated capability selector. Default value: Line1 (settable in the interface 'Line')
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		matrixLine_cmd_val = self._base.get_repcap_cmd_value(matrixLine, repcap.MatrixLine)
		return self._core.io.query_struct(f'CONFigure:LTE:SIGNaling<Instance>:CONNection:PCC:TM9:CMATrix:MIMO44:LINE{matrixLine_cmd_val}?', self.__class__.GetStruct())

	def clone(self) -> 'Line':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Line(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

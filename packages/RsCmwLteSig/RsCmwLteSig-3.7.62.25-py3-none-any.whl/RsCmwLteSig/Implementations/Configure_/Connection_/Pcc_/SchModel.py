from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SchModel:
	"""SchModel commands group definition. 5 total commands, 3 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("schModel", core, parent)

	@property
	def enable(self):
		"""enable commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_enable'):
			from .SchModel_.Enable import Enable
			self._enable = Enable(self._core, self._base)
		return self._enable

	@property
	def mselection(self):
		"""mselection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mselection'):
			from .SchModel_.Mselection import Mselection
			self._mselection = Mselection(self._core, self._base)
		return self._mselection

	@property
	def mimo(self):
		"""mimo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mimo'):
			from .SchModel_.Mimo import Mimo
			self._mimo = Mimo(self._core, self._base)
		return self._mimo

	# noinspection PyTypeChecker
	class ValueStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- H_11_Abs: float: Square of magnitude of h11 Range: 0 to 1
			- H_11_Phi: int: Phase of h11 Range: 0 deg to 345 deg, Unit: deg
			- H_12_Phi: int: Phase of h12 Range: 0 deg to 345 deg, Unit: deg
			- H_21_Abs: float: Square of magnitude of h21 Range: 0 to 1
			- H_21_Phi: int: Phase of h21 Range: 0 deg to 345 deg, Unit: deg
			- H_22_Phi: int: Phase of h22 Range: 0 deg to 345 deg, Unit: deg"""
		__meta_args_list = [
			ArgStruct.scalar_float('H_11_Abs'),
			ArgStruct.scalar_int('H_11_Phi'),
			ArgStruct.scalar_int('H_12_Phi'),
			ArgStruct.scalar_float('H_21_Abs'),
			ArgStruct.scalar_int('H_21_Phi'),
			ArgStruct.scalar_int('H_22_Phi')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.H_11_Abs: float = None
			self.H_11_Phi: int = None
			self.H_12_Phi: int = None
			self.H_21_Abs: float = None
			self.H_21_Phi: int = None
			self.H_22_Phi: int = None

	def get_value(self) -> ValueStruct:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:CONNection[:PCC]:SCHModel \n
		Snippet: value: ValueStruct = driver.configure.connection.pcc.schModel.get_value() \n
		Configures the channel coefficients, characterizing the radio channel for MIMO 2x2. \n
			:return: structure: for return value, see the help for ValueStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:LTE:SIGNaling<Instance>:CONNection:PCC:SCHModel?', self.__class__.ValueStruct())

	def set_value(self, value: ValueStruct) -> None:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:CONNection[:PCC]:SCHModel \n
		Snippet: driver.configure.connection.pcc.schModel.set_value(value = ValueStruct()) \n
		Configures the channel coefficients, characterizing the radio channel for MIMO 2x2. \n
			:param value: see the help for ValueStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:LTE:SIGNaling<Instance>:CONNection:PCC:SCHModel', value)

	def clone(self) -> 'SchModel':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SchModel(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

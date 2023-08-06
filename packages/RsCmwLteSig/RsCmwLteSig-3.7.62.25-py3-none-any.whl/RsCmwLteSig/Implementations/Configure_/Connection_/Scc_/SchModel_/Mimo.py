from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mimo:
	"""Mimo commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: Mimo, default value after init: Mimo.M42"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mimo", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_mimo_get', 'repcap_mimo_set', repcap.Mimo.M42)

	def repcap_mimo_set(self, enum_value: repcap.Mimo) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Mimo.Default
		Default value after init: Mimo.M42"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_mimo_get(self) -> repcap.Mimo:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	# noinspection PyTypeChecker
	class MimoStruct(StructBase):
		"""Structure for setting input parameters. Contains optional setting parameters. Fields: \n
			- H_11_Abs: float: Range: 0 to 1
			- H_11_Phi: int: Range: 0 deg to 345 deg, Unit: deg
			- H_12_Abs: float: Range: 0 to 1
			- H_12_Phi: int: Range: 0 deg to 345 deg, Unit: deg
			- H_13_Abs: float: Range: 0 to 1
			- H_13_Phi: int: Range: 0 deg to 345 deg, Unit: deg
			- H_14_Abs: float: Range: 0 to 1
			- H_14_Phi: int: Range: 0 deg to 345 deg, Unit: deg
			- H_21_Abs: float: Range: 0 to 1
			- H_21_Phi: int: Range: 0 deg to 345 deg, Unit: deg
			- H_22_Abs: float: Range: 0 to 1
			- H_22_Phi: int: Range: 0 deg to 345 deg, Unit: deg
			- H_23_Abs: float: Range: 0 to 1
			- H_23_Phi: int: Range: 0 deg to 345 deg, Unit: deg
			- H_24_Abs: float: Range: 0 to 1
			- H_24_Phi: int: Range: 0 deg to 345 deg, Unit: deg
			- H_31_Abs: float: Optional setting parameter. Range: 0 to 1
			- H_31_Phi: int: Optional setting parameter. Range: 0 deg to 345 deg, Unit: deg
			- H_32_Abs: float: Optional setting parameter. Range: 0 to 1
			- H_32_Phi: int: Optional setting parameter. Range: 0 deg to 345 deg, Unit: deg
			- H_33_Abs: float: Optional setting parameter. Range: 0 to 1
			- H_33_Phi: int: Optional setting parameter. Range: 0 deg to 345 deg, Unit: deg
			- H_34_Abs: float: Optional setting parameter. Range: 0 to 1
			- H_34_Phi: int: Optional setting parameter. Range: 0 deg to 345 deg, Unit: deg
			- H_41_Abs: float: Optional setting parameter. Range: 0 to 1
			- H_41_Phi: int: Optional setting parameter. Range: 0 deg to 345 deg, Unit: deg
			- H_42_Abs: float: Optional setting parameter. Range: 0 to 1
			- H_42_Phi: int: Optional setting parameter. Range: 0 deg to 345 deg, Unit: deg
			- H_43_Abs: float: Optional setting parameter. Range: 0 to 1
			- H_43_Phi: int: Optional setting parameter. Range: 0 deg to 345 deg, Unit: deg
			- H_44_Abs: float: Optional setting parameter. Range: 0 to 1
			- H_44_Phi: int: Optional setting parameter. Range: 0 deg to 345 deg, Unit: deg"""
		__meta_args_list = [
			ArgStruct.scalar_float('H_11_Abs'),
			ArgStruct.scalar_int('H_11_Phi'),
			ArgStruct.scalar_float('H_12_Abs'),
			ArgStruct.scalar_int('H_12_Phi'),
			ArgStruct.scalar_float('H_13_Abs'),
			ArgStruct.scalar_int('H_13_Phi'),
			ArgStruct.scalar_float('H_14_Abs'),
			ArgStruct.scalar_int('H_14_Phi'),
			ArgStruct.scalar_float('H_21_Abs'),
			ArgStruct.scalar_int('H_21_Phi'),
			ArgStruct.scalar_float('H_22_Abs'),
			ArgStruct.scalar_int('H_22_Phi'),
			ArgStruct.scalar_float('H_23_Abs'),
			ArgStruct.scalar_int('H_23_Phi'),
			ArgStruct.scalar_float('H_24_Abs'),
			ArgStruct.scalar_int('H_24_Phi'),
			ArgStruct.scalar_float('H_31_Abs'),
			ArgStruct.scalar_int('H_31_Phi'),
			ArgStruct.scalar_float('H_32_Abs'),
			ArgStruct.scalar_int('H_32_Phi'),
			ArgStruct.scalar_float('H_33_Abs'),
			ArgStruct.scalar_int('H_33_Phi'),
			ArgStruct.scalar_float('H_34_Abs'),
			ArgStruct.scalar_int('H_34_Phi'),
			ArgStruct.scalar_float('H_41_Abs'),
			ArgStruct.scalar_int('H_41_Phi'),
			ArgStruct.scalar_float('H_42_Abs'),
			ArgStruct.scalar_int('H_42_Phi'),
			ArgStruct.scalar_float('H_43_Abs'),
			ArgStruct.scalar_int('H_43_Phi'),
			ArgStruct.scalar_float('H_44_Abs'),
			ArgStruct.scalar_int('H_44_Phi')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.H_11_Abs: float = None
			self.H_11_Phi: int = None
			self.H_12_Abs: float = None
			self.H_12_Phi: int = None
			self.H_13_Abs: float = None
			self.H_13_Phi: int = None
			self.H_14_Abs: float = None
			self.H_14_Phi: int = None
			self.H_21_Abs: float = None
			self.H_21_Phi: int = None
			self.H_22_Abs: float = None
			self.H_22_Phi: int = None
			self.H_23_Abs: float = None
			self.H_23_Phi: int = None
			self.H_24_Abs: float = None
			self.H_24_Phi: int = None
			self.H_31_Abs: float = None
			self.H_31_Phi: int = None
			self.H_32_Abs: float = None
			self.H_32_Phi: int = None
			self.H_33_Abs: float = None
			self.H_33_Phi: int = None
			self.H_34_Abs: float = None
			self.H_34_Phi: int = None
			self.H_41_Abs: float = None
			self.H_41_Phi: int = None
			self.H_42_Abs: float = None
			self.H_42_Phi: int = None
			self.H_43_Abs: float = None
			self.H_43_Phi: int = None
			self.H_44_Abs: float = None
			self.H_44_Phi: int = None

	def set(self, structure: MimoStruct, secondaryCompCarrier=repcap.SecondaryCompCarrier.Default, mimo=repcap.Mimo.Default) -> None:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:CONNection:SCC<Carrier>:SCHModel:MIMO<Mimo> \n
		Snippet: driver.configure.connection.scc.schModel.mimo.set(value = [PROPERTY_STRUCT_NAME](), secondaryCompCarrier = repcap.SecondaryCompCarrier.Default, mimo = repcap.Mimo.Default) \n
		Configures the coefficients of the user-defined channel matrix, characterizing the radio channel for MIMO 4x2 or MIMO 4x4.
			INTRO_CMD_HELP: There are two types of parameters: \n
			- <hnmabs> defines the square of the magnitude of the channel coefficient nm: <hnmabs> = (hnm) 2 The sum of all <h1mabs> must equal 1: <h11abs> + <h12abs> + <h13abs> + <h14abs> = 1 The same applies to <h2mabs>, <h3mabs> and <h4mabs>.
			- <hnmphi> defines the phase of the channel coefficient nm: <hnmphi> = φ(hnm) The phase can be entered in steps of 15 degrees. The setting is rounded, if necessary.
		The *RST values depend on <Mimo> and are listed as *RST 4x2 / *RST 4x4. \n
			:param structure: for set value, see the help for MimoStruct structure arguments.
			:param secondaryCompCarrier: optional repeated capability selector. Default value: CC1 (settable in the interface 'Scc')
			:param mimo: optional repeated capability selector. Default value: M42 (settable in the interface 'Mimo')"""
		secondaryCompCarrier_cmd_val = self._base.get_repcap_cmd_value(secondaryCompCarrier, repcap.SecondaryCompCarrier)
		mimo_cmd_val = self._base.get_repcap_cmd_value(mimo, repcap.Mimo)
		self._core.io.write_struct(f'CONFigure:LTE:SIGNaling<Instance>:CONNection:SCC{secondaryCompCarrier_cmd_val}:SCHModel:MIMO{mimo_cmd_val}', structure)

	def get(self, secondaryCompCarrier=repcap.SecondaryCompCarrier.Default, mimo=repcap.Mimo.Default) -> MimoStruct:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:CONNection:SCC<Carrier>:SCHModel:MIMO<Mimo> \n
		Snippet: value: MimoStruct = driver.configure.connection.scc.schModel.mimo.get(secondaryCompCarrier = repcap.SecondaryCompCarrier.Default, mimo = repcap.Mimo.Default) \n
		Configures the coefficients of the user-defined channel matrix, characterizing the radio channel for MIMO 4x2 or MIMO 4x4.
			INTRO_CMD_HELP: There are two types of parameters: \n
			- <hnmabs> defines the square of the magnitude of the channel coefficient nm: <hnmabs> = (hnm) 2 The sum of all <h1mabs> must equal 1: <h11abs> + <h12abs> + <h13abs> + <h14abs> = 1 The same applies to <h2mabs>, <h3mabs> and <h4mabs>.
			- <hnmphi> defines the phase of the channel coefficient nm: <hnmphi> = φ(hnm) The phase can be entered in steps of 15 degrees. The setting is rounded, if necessary.
		The *RST values depend on <Mimo> and are listed as *RST 4x2 / *RST 4x4. \n
			:param secondaryCompCarrier: optional repeated capability selector. Default value: CC1 (settable in the interface 'Scc')
			:param mimo: optional repeated capability selector. Default value: M42 (settable in the interface 'Mimo')
			:return: structure: for return value, see the help for MimoStruct structure arguments."""
		secondaryCompCarrier_cmd_val = self._base.get_repcap_cmd_value(secondaryCompCarrier, repcap.SecondaryCompCarrier)
		mimo_cmd_val = self._base.get_repcap_cmd_value(mimo, repcap.Mimo)
		return self._core.io.query_struct(f'CONFigure:LTE:SIGNaling<Instance>:CONNection:SCC{secondaryCompCarrier_cmd_val}:SCHModel:MIMO{mimo_cmd_val}?', self.__class__.MimoStruct())

	def clone(self) -> 'Mimo':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Mimo(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

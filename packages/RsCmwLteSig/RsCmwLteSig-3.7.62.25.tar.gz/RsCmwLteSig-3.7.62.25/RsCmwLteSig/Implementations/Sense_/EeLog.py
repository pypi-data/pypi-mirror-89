from typing import List

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.Types import DataType
from ...Internal.StructBase import StructBase
from ...Internal.ArgStruct import ArgStruct
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EeLog:
	"""EeLog commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("eeLog", core, parent)

	# noinspection PyTypeChecker
	class LastStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Timestamp: str: No parameter help available
			- Category: enums.LogCategory2: No parameter help available
			- Event: str: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_str('Timestamp'),
			ArgStruct.scalar_enum('Category', enums.LogCategory2),
			ArgStruct.scalar_str('Event')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Timestamp: str = None
			self.Category: enums.LogCategory2 = None
			self.Event: str = None

	def get_last(self) -> LastStruct:
		"""SCPI: SENSe:LTE:SIGNaling<instance>:EELog:LAST \n
		Snippet: value: LastStruct = driver.sense.eeLog.get_last() \n
		No command help available \n
			:return: structure: for return value, see the help for LastStruct structure arguments.
		"""
		return self._core.io.query_struct('SENSe:LTE:SIGNaling<Instance>:EELog:LAST?', self.__class__.LastStruct())

	# noinspection PyTypeChecker
	class AllStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Timestamp: List[str]: No parameter help available
			- Category: List[enums.LogCategory2]: No parameter help available
			- Event: List[str]: No parameter help available"""
		__meta_args_list = [
			ArgStruct('Timestamp', DataType.StringList, None, False, True, 1),
			ArgStruct('Category', DataType.EnumList, enums.LogCategory2, False, True, 1),
			ArgStruct('Event', DataType.StringList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Timestamp: List[str] = None
			self.Category: List[enums.LogCategory2] = None
			self.Event: List[str] = None

	def get_all(self) -> AllStruct:
		"""SCPI: SENSe:LTE:SIGNaling<instance>:EELog:ALL \n
		Snippet: value: AllStruct = driver.sense.eeLog.get_all() \n
		No command help available \n
			:return: structure: for return value, see the help for AllStruct structure arguments.
		"""
		return self._core.io.query_struct('SENSe:LTE:SIGNaling<Instance>:EELog:ALL?', self.__class__.AllStruct())

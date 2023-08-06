from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IpAddress:
	"""IpAddress commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ipAddress", core, parent)

	def set(self, index: enums.IPADdress) -> None:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:MMONitor:IPADdress \n
		Snippet: driver.configure.mmonitor.ipAddress.set(index = enums.IPADdress.IP1) \n
		Selects the IP address to which signaling messages are sent for message monitoring. The address pool is configured
		globally via CONFigure:BASE:MMONitor:IPADdress<n>. A query returns both the current index and the resulting IP address. \n
			:param index: IP1 | IP2 | IP3 Address pool index
		"""
		param = Conversions.enum_scalar_to_str(index, enums.IPADdress)
		self._core.io.write(f'CONFigure:LTE:SIGNaling<Instance>:MMONitor:IPADdress {param}')

	# noinspection PyTypeChecker
	class GetStruct(StructBase):
		"""Response structure. Fields: \n
			- Index: enums.IPADdress: IP1 | IP2 | IP3 Address pool index
			- Ip_Address: str: Used IP address as string"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Index', enums.IPADdress),
			ArgStruct.scalar_str('Ip_Address')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Index: enums.IPADdress = None
			self.Ip_Address: str = None

	def get(self) -> GetStruct:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:MMONitor:IPADdress \n
		Snippet: value: GetStruct = driver.configure.mmonitor.ipAddress.get() \n
		Selects the IP address to which signaling messages are sent for message monitoring. The address pool is configured
		globally via CONFigure:BASE:MMONitor:IPADdress<n>. A query returns both the current index and the resulting IP address. \n
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:LTE:SIGNaling<Instance>:MMONitor:IPADdress?', self.__class__.GetStruct())

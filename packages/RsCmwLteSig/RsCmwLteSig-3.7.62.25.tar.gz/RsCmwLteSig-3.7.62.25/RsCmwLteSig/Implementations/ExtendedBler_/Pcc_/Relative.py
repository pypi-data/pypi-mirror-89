from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Relative:
	"""Relative commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("relative", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: See 'Reliability Indicator'
			- Ack: float: Received acknowledgments (percentage of sent scheduled subframes) Range: 0 % to 100 %, Unit: %
			- Nack: float: Received negative acknowledgments (percentage of sent scheduled subframes) Range: 0 % to 100 %, Unit: %
			- Bler: float: Block error ratio (percentage of sent scheduled subframes for which no ACK has been received) Range: 0 % to 100 %, Unit: %
			- Thougput_Avg_Rel: float: No parameter help available
			- Dtx: float: Percentage of sent scheduled subframes for which no ACK and no NACK has been received Range: 0 % to 100 %, Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Ack'),
			ArgStruct.scalar_float('Nack'),
			ArgStruct.scalar_float('Bler'),
			ArgStruct.scalar_float('Thougput_Avg_Rel'),
			ArgStruct.scalar_float('Dtx')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Ack: float = None
			self.Nack: float = None
			self.Bler: float = None
			self.Thougput_Avg_Rel: float = None
			self.Dtx: float = None

	def fetch(self) -> FetchStruct:
		"""SCPI: FETCh:LTE:SIGNaling<instance>:EBLer[:PCC]:RELative \n
		Snippet: value: FetchStruct = driver.extendedBler.pcc.relative.fetch() \n
		Returns the relative overall results of the BLER measurement for the sum of all DL streams of one carrier. The number to
		the left of each result parameter is provided for easy identification of the parameter position within the result array. \n
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		return self._core.io.query_struct(f'FETCh:LTE:SIGNaling<Instance>:EBLer:PCC:RELative?', self.__class__.FetchStruct())

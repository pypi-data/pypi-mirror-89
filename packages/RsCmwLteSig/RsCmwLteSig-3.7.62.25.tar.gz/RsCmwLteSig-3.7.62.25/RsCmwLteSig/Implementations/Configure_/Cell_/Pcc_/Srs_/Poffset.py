from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Poffset:
	"""Poffset commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("poffset", core, parent)

	def set(self, offset: int) -> None:
		"""SCPI: CONFigure:LTE:SIGNaling<Instance>:CELL[:PCC]:SRS:POFFset \n
		Snippet: driver.configure.cell.pcc.srs.poffset.set(offset = 1) \n
		Specifies the 'pSRS-Offset' value. The setting is only used if manual configuration is enabled,
		see CONFigure:LTE:SIGN<i>:SRS:MCENable. A query returns <Offset>, <Value>. \n
			:param offset: 'pSRS-Offset' value Range: 0 to 15
		"""
		param = Conversions.decimal_value_to_str(offset)
		self._core.io.write(f'CONFigure:LTE:SIGNaling<Instance>:CELL:PCC:SRS:POFFset {param}')

	# noinspection PyTypeChecker
	class GetStruct(StructBase):
		"""Response structure. Fields: \n
			- Offset: int: 'pSRS-Offset' value Range: 0 to 15
			- Value: float: Offset in dB, corresponding to the configured 'pSRS-Offset' value Range: -10.5 dB to 12 dB, Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_int('Offset'),
			ArgStruct.scalar_float('Value')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Offset: int = None
			self.Value: float = None

	def get(self) -> GetStruct:
		"""SCPI: CONFigure:LTE:SIGNaling<Instance>:CELL[:PCC]:SRS:POFFset \n
		Snippet: value: GetStruct = driver.configure.cell.pcc.srs.poffset.get() \n
		Specifies the 'pSRS-Offset' value. The setting is only used if manual configuration is enabled,
		see CONFigure:LTE:SIGN<i>:SRS:MCENable. A query returns <Offset>, <Value>. \n
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:LTE:SIGNaling<Instance>:CELL:PCC:SRS:POFFset?', self.__class__.GetStruct())

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pucch:
	"""Pucch commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pucch", core, parent)

	# noinspection PyTypeChecker
	def get_ffca(self) -> enums.PucchFormat:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:CONNection[:PCC]:PUCCh:FFCA \n
		Snippet: value: enums.PucchFormat = driver.configure.connection.pcc.pucch.get_ffca() \n
		Selects the PUCCH format used for carrier aggregation scenarios. \n
			:return: format_py: F1BCs | F3 | F4 | F5 F1BCs: PUCCH format 1b with channel selection (if allowed) F3: PUCCH format 3 F4: PUCCH format 4 F5: PUCCH format 5
		"""
		response = self._core.io.query_str('CONFigure:LTE:SIGNaling<Instance>:CONNection:PCC:PUCCh:FFCA?')
		return Conversions.str_to_scalar_enum(response, enums.PucchFormat)

	def set_ffca(self, format_py: enums.PucchFormat) -> None:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:CONNection[:PCC]:PUCCh:FFCA \n
		Snippet: driver.configure.connection.pcc.pucch.set_ffca(format_py = enums.PucchFormat.F1BCs) \n
		Selects the PUCCH format used for carrier aggregation scenarios. \n
			:param format_py: F1BCs | F3 | F4 | F5 F1BCs: PUCCH format 1b with channel selection (if allowed) F3: PUCCH format 3 F4: PUCCH format 4 F5: PUCCH format 5
		"""
		param = Conversions.enum_scalar_to_str(format_py, enums.PucchFormat)
		self._core.io.write(f'CONFigure:LTE:SIGNaling<Instance>:CONNection:PCC:PUCCh:FFCA {param}')

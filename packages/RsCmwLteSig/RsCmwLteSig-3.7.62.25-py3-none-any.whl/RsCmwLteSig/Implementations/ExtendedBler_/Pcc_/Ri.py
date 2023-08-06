from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ri:
	"""Ri commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ri", core, parent)

	def fetch(self) -> List[int]:
		"""SCPI: FETCh:LTE:SIGNaling<instance>:EBLer[:PCC]:RI \n
		Snippet: value: List[int] = driver.extendedBler.pcc.ri.fetch() \n
		Returns the rank indicator (RI) results. \n
		Use RsCmwLteSig.reliability.last_value to read the updated reliability indicator. \n
			:return: ri: Comma-separated list of four values: Number of received 'RI = 1' Number of received 'RI = 2' Number of received 'RI = 3' Number of received 'RI = 4' Range: 0 to 2E+9"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_int_list_suppressed(f'FETCh:LTE:SIGNaling<Instance>:EBLer:PCC:RI?', suppressed)
		return response

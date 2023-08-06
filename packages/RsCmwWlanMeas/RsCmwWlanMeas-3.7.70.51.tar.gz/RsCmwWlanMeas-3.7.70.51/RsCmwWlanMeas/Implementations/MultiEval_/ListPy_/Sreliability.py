from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sreliability:
	"""Sreliability commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sreliability", core, parent)

	def fetch(self) -> List[int]:
		"""SCPI: FETCh:WLAN:MEASurement<Instance>:MEValuation:LIST:SRELiability \n
		Snippet: value: List[int] = driver.multiEval.listPy.sreliability.fetch() \n
		No command help available \n
		Use RsCmwWlanMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: seg_reliabilities: No help available"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_int_list_suppressed(f'FETCh:WLAN:MEASurement<Instance>:MEValuation:LIST:SRELiability?', suppressed)
		return response

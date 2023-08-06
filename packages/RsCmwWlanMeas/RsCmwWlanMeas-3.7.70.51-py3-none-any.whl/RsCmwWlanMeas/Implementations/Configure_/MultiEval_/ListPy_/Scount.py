from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Scount:
	"""Scount commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scount", core, parent)

	def get_modulation(self) -> List[int]:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SCOunt:MODulation \n
		Snippet: value: List[int] = driver.configure.multiEval.listPy.scount.get_modulation() \n
		No command help available \n
			:return: stat_counts_mod: No help available
		"""
		response = self._core.io.query_bin_or_ascii_int_list('CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SCOunt:MODulation?')
		return response

	def set_modulation(self, stat_counts_mod: List[int]) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SCOunt:MODulation \n
		Snippet: driver.configure.multiEval.listPy.scount.set_modulation(stat_counts_mod = [1, 2, 3]) \n
		No command help available \n
			:param stat_counts_mod: No help available
		"""
		param = Conversions.list_to_csv_str(stat_counts_mod)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SCOunt:MODulation {param}')

	def get_ts_mask(self) -> List[int]:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SCOunt:TSMask \n
		Snippet: value: List[int] = driver.configure.multiEval.listPy.scount.get_ts_mask() \n
		No command help available \n
			:return: stat_counts_sem: No help available
		"""
		response = self._core.io.query_bin_or_ascii_int_list('CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SCOunt:TSMask?')
		return response

	def set_ts_mask(self, stat_counts_sem: List[int]) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SCOunt:TSMask \n
		Snippet: driver.configure.multiEval.listPy.scount.set_ts_mask(stat_counts_sem = [1, 2, 3]) \n
		No command help available \n
			:param stat_counts_sem: No help available
		"""
		param = Conversions.list_to_csv_str(stat_counts_sem)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SCOunt:TSMask {param}')

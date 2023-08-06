from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ListPy:
	"""ListPy commands group definition. 30 total commands, 4 Sub-groups, 12 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("listPy", core, parent)

	@property
	def segment(self):
		"""segment commands group. 13 Sub-classes, 0 commands."""
		if not hasattr(self, '_segment'):
			from .ListPy_.Segment import Segment
			self._segment = Segment(self._core, self._base)
		return self._segment

	@property
	def singleCmw(self):
		"""singleCmw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_singleCmw'):
			from .ListPy_.SingleCmw import SingleCmw
			self._singleCmw = SingleCmw(self._core, self._base)
		return self._singleCmw

	@property
	def scount(self):
		"""scount commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_scount'):
			from .ListPy_.Scount import Scount
			self._scount = Scount(self._core, self._base)
		return self._scount

	@property
	def result(self):
		"""result commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_result'):
			from .ListPy_.Result import Result
			self._result = Result(self._core, self._base)
		return self._result

	def get_count(self) -> int:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:COUNt \n
		Snippet: value: int = driver.configure.multiEval.listPy.get_count() \n
		No command help available \n
			:return: no_of_segments: No help available
		"""
		response = self._core.io.query_str('CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:COUNt?')
		return Conversions.str_to_int(response)

	def set_count(self, no_of_segments: int) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:COUNt \n
		Snippet: driver.configure.multiEval.listPy.set_count(no_of_segments = 1) \n
		No command help available \n
			:param no_of_segments: No help available
		"""
		param = Conversions.decimal_value_to_str(no_of_segments)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:COUNt {param}')

	# noinspection PyTypeChecker
	def get_cmode(self) -> enums.ParameterSetMode:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:CMODe \n
		Snippet: value: enums.ParameterSetMode = driver.configure.multiEval.listPy.get_cmode() \n
		No command help available \n
			:return: connector_mode: No help available
		"""
		response = self._core.io.query_str('CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:CMODe?')
		return Conversions.str_to_scalar_enum(response, enums.ParameterSetMode)

	def set_cmode(self, connector_mode: enums.ParameterSetMode) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:CMODe \n
		Snippet: driver.configure.multiEval.listPy.set_cmode(connector_mode = enums.ParameterSetMode.GLOBal) \n
		No command help available \n
			:param connector_mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(connector_mode, enums.ParameterSetMode)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:CMODe {param}')

	def get_stime(self) -> List[float]:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:STIMe \n
		Snippet: value: List[float] = driver.configure.multiEval.listPy.get_stime() \n
		No command help available \n
			:return: segment_times: No help available
		"""
		response = self._core.io.query_bin_or_ascii_float_list('CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:STIMe?')
		return response

	def set_stime(self, segment_times: List[float]) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:STIMe \n
		Snippet: driver.configure.multiEval.listPy.set_stime(segment_times = [1.1, 2.2, 3.3]) \n
		No command help available \n
			:param segment_times: No help available
		"""
		param = Conversions.list_to_csv_str(segment_times)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:STIMe {param}')

	def get_mtime(self) -> List[float]:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:MTIMe \n
		Snippet: value: List[float] = driver.configure.multiEval.listPy.get_mtime() \n
		No command help available \n
			:return: meas_times: No help available
		"""
		response = self._core.io.query_bin_or_ascii_float_list('CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:MTIMe?')
		return response

	def set_mtime(self, meas_times: List[float]) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:MTIMe \n
		Snippet: driver.configure.multiEval.listPy.set_mtime(meas_times = [1.1, 2.2, 3.3]) \n
		No command help available \n
			:param meas_times: No help available
		"""
		param = Conversions.list_to_csv_str(meas_times)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:MTIMe {param}')

	def get_moffset(self) -> List[float]:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:MOFFset \n
		Snippet: value: List[float] = driver.configure.multiEval.listPy.get_moffset() \n
		No command help available \n
			:return: meas_offsets: No help available
		"""
		response = self._core.io.query_bin_or_ascii_float_list('CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:MOFFset?')
		return response

	def set_moffset(self, meas_offsets: List[float]) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:MOFFset \n
		Snippet: driver.configure.multiEval.listPy.set_moffset(meas_offsets = [1.1, 2.2, 3.3]) \n
		No command help available \n
			:param meas_offsets: No help available
		"""
		param = Conversions.list_to_csv_str(meas_offsets)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:MOFFset {param}')

	def get_envelope_power(self) -> List[float]:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:ENPower \n
		Snippet: value: List[float] = driver.configure.multiEval.listPy.get_envelope_power() \n
		No command help available \n
			:return: levels: No help available
		"""
		response = self._core.io.query_bin_or_ascii_float_list('CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:ENPower?')
		return response

	def set_envelope_power(self, levels: List[float]) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:ENPower \n
		Snippet: driver.configure.multiEval.listPy.set_envelope_power(levels = [1.1, 2.2, 3.3]) \n
		No command help available \n
			:param levels: No help available
		"""
		param = Conversions.list_to_csv_str(levels)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:ENPower {param}')

	def get_frequency(self) -> List[float]:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:FREQuency \n
		Snippet: value: List[float] = driver.configure.multiEval.listPy.get_frequency() \n
		No command help available \n
			:return: frequencies: No help available
		"""
		response = self._core.io.query_bin_or_ascii_float_list('CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:FREQuency?')
		return response

	def set_frequency(self, frequencies: List[float]) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:FREQuency \n
		Snippet: driver.configure.multiEval.listPy.set_frequency(frequencies = [1.1, 2.2, 3.3]) \n
		No command help available \n
			:param frequencies: No help available
		"""
		param = Conversions.list_to_csv_str(frequencies)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:FREQuency {param}')

	# noinspection PyTypeChecker
	def get_standard(self) -> List[enums.IeeeStandard]:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:STANdard \n
		Snippet: value: List[enums.IeeeStandard] = driver.configure.multiEval.listPy.get_standard() \n
		No command help available \n
			:return: standards: No help available
		"""
		response = self._core.io.query_str('CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:STANdard?')
		return Conversions.str_to_list_enum(response, enums.IeeeStandard)

	def set_standard(self, standards: List[enums.IeeeStandard]) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:STANdard \n
		Snippet: driver.configure.multiEval.listPy.set_standard(standards = [IeeeStandard.DSSS, IeeeStandard.VHTofdm]) \n
		No command help available \n
			:param standards: No help available
		"""
		param = Conversions.enum_list_to_str(standards, enums.IeeeStandard)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:STANdard {param}')

	# noinspection PyTypeChecker
	def get_bandwidth(self) -> List[enums.Bandwidth]:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:BWIDth \n
		Snippet: value: List[enums.Bandwidth] = driver.configure.multiEval.listPy.get_bandwidth() \n
		No command help available \n
			:return: band_widths: No help available
		"""
		response = self._core.io.query_str('CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:BWIDth?')
		return Conversions.str_to_list_enum(response, enums.Bandwidth)

	def set_bandwidth(self, band_widths: List[enums.Bandwidth]) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:BWIDth \n
		Snippet: driver.configure.multiEval.listPy.set_bandwidth(band_widths = [Bandwidth.BW05mhz, Bandwidth.BW88mhz]) \n
		No command help available \n
			:param band_widths: No help available
		"""
		param = Conversions.enum_list_to_str(band_widths, enums.Bandwidth)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:BWIDth {param}')

	# noinspection PyTypeChecker
	def get_btype(self) -> List[enums.BurstTypeB]:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:BTYPe \n
		Snippet: value: List[enums.BurstTypeB] = driver.configure.multiEval.listPy.get_btype() \n
		No command help available \n
			:return: burst_types: No help available
		"""
		response = self._core.io.query_str('CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:BTYPe?')
		return Conversions.str_to_list_enum(response, enums.BurstTypeB)

	def set_btype(self, burst_types: List[enums.BurstTypeB]) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:BTYPe \n
		Snippet: driver.configure.multiEval.listPy.set_btype(burst_types = [BurstTypeB.GREenfield, BurstTypeB.MIXed]) \n
		No command help available \n
			:param burst_types: No help available
		"""
		param = Conversions.enum_list_to_str(burst_types, enums.BurstTypeB)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:BTYPe {param}')

	def get_rtrigger(self) -> List[bool]:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:RTRigger \n
		Snippet: value: List[bool] = driver.configure.multiEval.listPy.get_rtrigger() \n
		No command help available \n
			:return: re_triggers: No help available
		"""
		response = self._core.io.query_str('CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:RTRigger?')
		return Conversions.str_to_bool_list(response)

	def set_rtrigger(self, re_triggers: List[bool]) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:RTRigger \n
		Snippet: driver.configure.multiEval.listPy.set_rtrigger(re_triggers = [True, False, True]) \n
		No command help available \n
			:param re_triggers: No help available
		"""
		param = Conversions.list_to_csv_str(re_triggers)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:RTRigger {param}')

	def get_value(self) -> bool:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST \n
		Snippet: value: bool = driver.configure.multiEval.listPy.get_value() \n
		No command help available \n
			:return: list_mode_enable: No help available
		"""
		response = self._core.io.query_str('CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST?')
		return Conversions.str_to_bool(response)

	def set_value(self, list_mode_enable: bool) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST \n
		Snippet: driver.configure.multiEval.listPy.set_value(list_mode_enable = False) \n
		No command help available \n
			:param list_mode_enable: No help available
		"""
		param = Conversions.bool_to_str(list_mode_enable)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST {param}')

	def clone(self) -> 'ListPy':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ListPy(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

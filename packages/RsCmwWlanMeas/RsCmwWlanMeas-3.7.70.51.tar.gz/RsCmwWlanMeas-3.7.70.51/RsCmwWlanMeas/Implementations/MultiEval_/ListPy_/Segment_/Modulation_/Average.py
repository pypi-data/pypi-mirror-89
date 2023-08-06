from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Average:
	"""Average commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("average", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: No parameter help available
			- Seg_Reliability: int: No parameter help available
			- Out_Of_Tol: float: No parameter help available
			- Mcs_Index: int: No parameter help available
			- Mod_Type: enums.ModulationTypeD: No parameter help available
			- Payload_Sym: int: No parameter help available
			- Measured_Sym: int: No parameter help available
			- Payload_Bytes: int: No parameter help available
			- Guard_Interval: enums.GuardInterval: No parameter help available
			- No_Ss: int: No parameter help available
			- No_Of_Sts: int: No parameter help available
			- Burst_Rate: float: No parameter help available
			- Power_Backoff: float: No parameter help available
			- Burst_Power: float: No parameter help available
			- Peak_Power: float: No parameter help available
			- Crest_Factor: float: No parameter help available
			- Evm_All_Carr: float: No parameter help available
			- Evm_Data_Carr: float: No parameter help available
			- Evm_Pilot_Carr: float: No parameter help available
			- Freq_Error: float: No parameter help available
			- Clock_Error: float: No parameter help available
			- Iq_Offset: float: No parameter help available
			- Dc_Power: float: No parameter help available
			- Gain_Imbalance: float: No parameter help available
			- Quad_Error: float: No parameter help available
			- Ltf_Power: float: No parameter help available
			- Data_Power: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Seg_Reliability'),
			ArgStruct.scalar_float('Out_Of_Tol'),
			ArgStruct.scalar_int('Mcs_Index'),
			ArgStruct.scalar_enum('Mod_Type', enums.ModulationTypeD),
			ArgStruct.scalar_int('Payload_Sym'),
			ArgStruct.scalar_int('Measured_Sym'),
			ArgStruct.scalar_int('Payload_Bytes'),
			ArgStruct.scalar_enum('Guard_Interval', enums.GuardInterval),
			ArgStruct.scalar_int('No_Ss'),
			ArgStruct.scalar_int('No_Of_Sts'),
			ArgStruct.scalar_float('Burst_Rate'),
			ArgStruct.scalar_float('Power_Backoff'),
			ArgStruct.scalar_float('Burst_Power'),
			ArgStruct.scalar_float('Peak_Power'),
			ArgStruct.scalar_float('Crest_Factor'),
			ArgStruct.scalar_float('Evm_All_Carr'),
			ArgStruct.scalar_float('Evm_Data_Carr'),
			ArgStruct.scalar_float('Evm_Pilot_Carr'),
			ArgStruct.scalar_float('Freq_Error'),
			ArgStruct.scalar_float('Clock_Error'),
			ArgStruct.scalar_float('Iq_Offset'),
			ArgStruct.scalar_float('Dc_Power'),
			ArgStruct.scalar_float('Gain_Imbalance'),
			ArgStruct.scalar_float('Quad_Error'),
			ArgStruct.scalar_float('Ltf_Power'),
			ArgStruct.scalar_float('Data_Power')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Seg_Reliability: int = None
			self.Out_Of_Tol: float = None
			self.Mcs_Index: int = None
			self.Mod_Type: enums.ModulationTypeD = None
			self.Payload_Sym: int = None
			self.Measured_Sym: int = None
			self.Payload_Bytes: int = None
			self.Guard_Interval: enums.GuardInterval = None
			self.No_Ss: int = None
			self.No_Of_Sts: int = None
			self.Burst_Rate: float = None
			self.Power_Backoff: float = None
			self.Burst_Power: float = None
			self.Peak_Power: float = None
			self.Crest_Factor: float = None
			self.Evm_All_Carr: float = None
			self.Evm_Data_Carr: float = None
			self.Evm_Pilot_Carr: float = None
			self.Freq_Error: float = None
			self.Clock_Error: float = None
			self.Iq_Offset: float = None
			self.Dc_Power: float = None
			self.Gain_Imbalance: float = None
			self.Quad_Error: float = None
			self.Ltf_Power: float = None
			self.Data_Power: float = None

	def fetch(self, segmentB=repcap.SegmentB.Default) -> FetchStruct:
		"""SCPI: FETCh:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent<segment>:MODulation:AVERage \n
		Snippet: value: FetchStruct = driver.multiEval.listPy.segment.modulation.average.fetch(segmentB = repcap.SegmentB.Default) \n
		No command help available \n
			:param segmentB: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		segmentB_cmd_val = self._base.get_repcap_cmd_value(segmentB, repcap.SegmentB)
		return self._core.io.query_struct(f'FETCh:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent{segmentB_cmd_val}:MODulation:AVERage?', self.__class__.FetchStruct())

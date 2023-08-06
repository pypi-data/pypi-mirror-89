from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Setup:
	"""Setup commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("setup", core, parent)

	# noinspection PyTypeChecker
	class SetupStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Segment_Time: float: No parameter help available
			- Meas_Time: float: No parameter help available
			- Meas_Offset: float: No parameter help available
			- Level: float: No parameter help available
			- Frequency: float: No parameter help available
			- Standard: enums.IeeeStandard: No parameter help available
			- Band_Width: enums.Bandwidth: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_float('Segment_Time'),
			ArgStruct.scalar_float('Meas_Time'),
			ArgStruct.scalar_float('Meas_Offset'),
			ArgStruct.scalar_float('Level'),
			ArgStruct.scalar_float('Frequency'),
			ArgStruct.scalar_enum('Standard', enums.IeeeStandard),
			ArgStruct.scalar_enum('Band_Width', enums.Bandwidth)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Segment_Time: float = None
			self.Meas_Time: float = None
			self.Meas_Offset: float = None
			self.Level: float = None
			self.Frequency: float = None
			self.Standard: enums.IeeeStandard = None
			self.Band_Width: enums.Bandwidth = None

	def set(self, structure: SetupStruct, segmentB=repcap.SegmentB.Default) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent<segment>:SETup \n
		Snippet: driver.configure.multiEval.listPy.segment.setup.set(value = [PROPERTY_STRUCT_NAME](), segmentB = repcap.SegmentB.Default) \n
		No command help available \n
			:param structure: for set value, see the help for SetupStruct structure arguments.
			:param segmentB: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')"""
		segmentB_cmd_val = self._base.get_repcap_cmd_value(segmentB, repcap.SegmentB)
		self._core.io.write_struct(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent{segmentB_cmd_val}:SETup', structure)

	def get(self, segmentB=repcap.SegmentB.Default) -> SetupStruct:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent<segment>:SETup \n
		Snippet: value: SetupStruct = driver.configure.multiEval.listPy.segment.setup.get(segmentB = repcap.SegmentB.Default) \n
		No command help available \n
			:param segmentB: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for SetupStruct structure arguments."""
		segmentB_cmd_val = self._base.get_repcap_cmd_value(segmentB, repcap.SegmentB)
		return self._core.io.query_struct(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent{segmentB_cmd_val}:SETup?', self.__class__.SetupStruct())

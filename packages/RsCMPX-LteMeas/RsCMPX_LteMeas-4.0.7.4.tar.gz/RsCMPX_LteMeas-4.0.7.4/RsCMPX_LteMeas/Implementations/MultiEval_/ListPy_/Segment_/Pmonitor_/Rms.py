from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rms:
	"""Rms commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rms", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Seg_Reliability: int: Reliability indicator for the segment
			- Step_Rms_Power: List[float]: Comma-separated list of power values, one value per subframe, from first to last subframe of the segment. For an inactive segment, only one INV is returned, independent of the number of configured subframes."""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Seg_Reliability'),
			ArgStruct('Step_Rms_Power', DataType.FloatList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Seg_Reliability: int = None
			self.Step_Rms_Power: List[float] = None

	def fetch(self, segment=repcap.Segment.Default) -> FetchStruct:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>:PMONitor:RMS \n
		Snippet: value: FetchStruct = driver.multiEval.listPy.segment.pmonitor.rms.fetch(segment = repcap.Segment.Default) \n
		Return the power monitor results for segment <no> in list mode. The commands return one power result for each subframe of
		the segment for the measured carrier. The power values are RMS averaged over the subframe or represent the peak value
		within the subframe. \n
			:param segment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		return self._core.io.query_struct(f'FETCh:LTE:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:PMONitor:RMS?', self.__class__.FetchStruct())

from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Positiv:
	"""Positiv commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("positiv", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Seg_Reliability: int: Reliability indicator for the segment
			- Statist_Expired: int: Reached statistical length in slots
			- Out_Of_Tolerance: int: Percentage of measured subframes with failed limit check
			- Margin_Avg_Pos_X: List[float]: No parameter help available
			- Margin_Avg_Pos_Y: List[float]: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Seg_Reliability'),
			ArgStruct.scalar_int('Statist_Expired'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct('Margin_Avg_Pos_X', DataType.FloatList, None, False, True, 1),
			ArgStruct('Margin_Avg_Pos_Y', DataType.FloatList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Seg_Reliability: int = None
			self.Statist_Expired: int = None
			self.Out_Of_Tolerance: int = None
			self.Margin_Avg_Pos_X: List[float] = None
			self.Margin_Avg_Pos_Y: List[float] = None

	def fetch(self, segment=repcap.Segment.Default) -> FetchStruct:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>:SEMask:MARGin:AVERage:POSitiv \n
		Snippet: value: FetchStruct = driver.multiEval.listPy.segment.seMask.margin.average.positiv.fetch(segment = repcap.Segment.Default) \n
		Return spectrum emission mask margin results for segment <no> in list mode. The individual commands provide results for
		the CURRent, AVERage and maximum traces (resulting in MINimum margins) for NEGative and POSitive offset frequencies.
		Returned sequence: <Reliability>, <SegReliability>, <StatistExpired>, <OutOfTolerance>, {<MarginX>, <MarginY>}area1, {...
		}area2, ..., {...}area12 \n
			:param segment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		return self._core.io.query_struct(f'FETCh:LTE:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:SEMask:MARGin:AVERage:POSitiv?', self.__class__.FetchStruct())

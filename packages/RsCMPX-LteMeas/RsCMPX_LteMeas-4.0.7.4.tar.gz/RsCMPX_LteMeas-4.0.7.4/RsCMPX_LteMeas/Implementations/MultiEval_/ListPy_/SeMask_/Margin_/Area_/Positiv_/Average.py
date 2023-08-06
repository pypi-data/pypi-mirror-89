from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Average:
	"""Average commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("average", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Margin_Avg_Pos_X: List[float]: X-position of margin for selected area
			- Margin_Avg_Pos_Y: List[float]: Y-position of margin for selected area"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct('Margin_Avg_Pos_X', DataType.FloatList, None, False, True, 1),
			ArgStruct('Margin_Avg_Pos_Y', DataType.FloatList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Margin_Avg_Pos_X: List[float] = None
			self.Margin_Avg_Pos_Y: List[float] = None

	def fetch(self, area=repcap.Area.Default) -> FetchStruct:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:LIST:SEMask:MARGin:AREA<nr>:POSitiv:AVERage \n
		Snippet: value: FetchStruct = driver.multiEval.listPy.seMask.margin.area.positiv.average.fetch(area = repcap.Area.Default) \n
		Return spectrum emission mask margin positions for all measured list mode segments. The individual commands provide
		results for the CURRent, AVERage and maximum traces (resulting in MINimum margins) for NEGative and POSitive offset
		frequencies. The results are returned as pairs per segment: <Reliability>, {<MarginPosX>, <MarginPosY>}Seg 1,
		{<MarginPosX>, <MarginPosY>}Seg 2, ... \n
			:param area: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Area')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		area_cmd_val = self._base.get_repcap_cmd_value(area, repcap.Area)
		return self._core.io.query_struct(f'FETCh:LTE:MEASurement<Instance>:MEValuation:LIST:SEMask:MARGin:AREA{area_cmd_val}:POSitiv:AVERage?', self.__class__.FetchStruct())

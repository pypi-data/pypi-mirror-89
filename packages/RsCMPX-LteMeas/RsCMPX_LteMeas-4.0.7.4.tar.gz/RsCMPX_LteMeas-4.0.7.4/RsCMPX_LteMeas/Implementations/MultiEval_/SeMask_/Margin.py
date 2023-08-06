from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Margin:
	"""Margin commands group definition. 8 total commands, 4 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("margin", core, parent)

	@property
	def all(self):
		"""all commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_all'):
			from .Margin_.All import All
			self._all = All(self._core, self._base)
		return self._all

	@property
	def current(self):
		"""current commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_current'):
			from .Margin_.Current import Current
			self._current = Current(self._core, self._base)
		return self._current

	@property
	def average(self):
		"""average commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_average'):
			from .Margin_.Average import Average
			self._average = Average(self._core, self._base)
		return self._average

	@property
	def minimum(self):
		"""minimum commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_minimum'):
			from .Margin_.Minimum import Minimum
			self._minimum = Minimum(self._core, self._base)
		return self._minimum

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: No parameter help available
			- Out_Of_Tolerance: int: No parameter help available
			- Margin_Curr_Neg: List[float]: No parameter help available
			- Margin_Curr_Pos: List[float]: No parameter help available
			- Margin_Avg_Neg: List[float]: No parameter help available
			- Margin_Avg_Pos: List[float]: No parameter help available
			- Margin_Min_Neg: List[float]: No parameter help available
			- Margin_Min_Pos: List[float]: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct('Margin_Curr_Neg', DataType.FloatList, None, False, False, 10),
			ArgStruct('Margin_Curr_Pos', DataType.FloatList, None, False, False, 10),
			ArgStruct('Margin_Avg_Neg', DataType.FloatList, None, False, False, 10),
			ArgStruct('Margin_Avg_Pos', DataType.FloatList, None, False, False, 10),
			ArgStruct('Margin_Min_Neg', DataType.FloatList, None, False, False, 10),
			ArgStruct('Margin_Min_Pos', DataType.FloatList, None, False, False, 10)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tolerance: int = None
			self.Margin_Curr_Neg: List[float] = None
			self.Margin_Curr_Pos: List[float] = None
			self.Margin_Avg_Neg: List[float] = None
			self.Margin_Avg_Pos: List[float] = None
			self.Margin_Min_Neg: List[float] = None
			self.Margin_Min_Pos: List[float] = None

	def fetch(self) -> FetchStruct:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:SEMask:MARGin \n
		Snippet: value: FetchStruct = driver.multiEval.seMask.margin.fetch() \n
		No command help available \n
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		return self._core.io.query_struct(f'FETCh:LTE:MEASurement<Instance>:MEValuation:SEMask:MARGin?', self.__class__.FetchStruct())

	def clone(self) -> 'Margin':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Margin(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

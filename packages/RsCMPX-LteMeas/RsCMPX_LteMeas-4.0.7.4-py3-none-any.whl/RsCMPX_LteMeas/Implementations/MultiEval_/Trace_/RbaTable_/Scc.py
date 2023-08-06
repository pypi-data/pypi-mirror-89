from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Scc:
	"""Scc commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scc", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: No parameter help available
			- Channel_Type: List[enums.RbTableChannelType]: No parameter help available
			- Offset_Rb: List[int]: No parameter help available
			- No_Rb: List[int]: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct('Channel_Type', DataType.EnumList, enums.RbTableChannelType, False, True, 1),
			ArgStruct('Offset_Rb', DataType.IntegerList, None, False, True, 1),
			ArgStruct('No_Rb', DataType.IntegerList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Channel_Type: List[enums.RbTableChannelType] = None
			self.Offset_Rb: List[int] = None
			self.No_Rb: List[int] = None

	def read(self) -> ResultData:
		"""SCPI: READ:LTE:MEASurement<Instance>:MEValuation:TRACe:RBATable:SCC \n
		Snippet: value: ResultData = driver.multiEval.trace.rbaTable.scc.read() \n
		No command help available \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:LTE:MEASurement<Instance>:MEValuation:TRACe:RBATable:SCC?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:TRACe:RBATable:SCC \n
		Snippet: value: ResultData = driver.multiEval.trace.rbaTable.scc.fetch() \n
		No command help available \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:LTE:MEASurement<Instance>:MEValuation:TRACe:RBATable:SCC?', self.__class__.ResultData())

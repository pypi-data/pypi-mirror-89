from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StandardDev:
	"""StandardDev commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("standardDev", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: No parameter help available
			- Out_Of_Tolerance: int: No parameter help available
			- Margin: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_float('Margin')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tolerance: int = None
			self.Margin: float = None

	def fetch(self) -> FetchStruct:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:IEMission:ULCA[:PCC]:MARGin:SDEViation \n
		Snippet: value: FetchStruct = driver.multiEval.inbandEmission.ulca.pcc.margin.standardDev.fetch() \n
		No command help available \n
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		return self._core.io.query_struct(f'FETCh:LTE:MEASurement<Instance>:MEValuation:IEMission:ULCA:PCC:MARGin:SDEViation?', self.__class__.FetchStruct())

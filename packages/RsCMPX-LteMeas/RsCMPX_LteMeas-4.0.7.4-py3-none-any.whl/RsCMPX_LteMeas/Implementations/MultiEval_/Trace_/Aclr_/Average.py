from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Average:
	"""Average commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("average", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Utra_2_Neg: float: Power in the second UTRA channel with lower frequency
			- Utra_1_Neg: float: Power in the first UTRA channel with lower frequency
			- Eutraneg: float: Power in the first E-UTRA channel with lower frequency
			- Eutra: float: Power in the allocated E-UTRA channel
			- Eutrapos: float: Power in the first E-UTRA channel with higher frequency
			- Utra_1_Pos: float: Power in the first UTRA channel with higher frequency
			- Utra_2_Pos: float: Power in the second UTRA channel with higher frequency"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Utra_2_Neg'),
			ArgStruct.scalar_float('Utra_1_Neg'),
			ArgStruct.scalar_float('Eutraneg'),
			ArgStruct.scalar_float('Eutra'),
			ArgStruct.scalar_float('Eutrapos'),
			ArgStruct.scalar_float('Utra_1_Pos'),
			ArgStruct.scalar_float('Utra_2_Pos')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Utra_2_Neg: float = None
			self.Utra_1_Neg: float = None
			self.Eutraneg: float = None
			self.Eutra: float = None
			self.Eutrapos: float = None
			self.Utra_1_Pos: float = None
			self.Utra_2_Pos: float = None

	def read(self) -> ResultData:
		"""SCPI: READ:LTE:MEASurement<Instance>:MEValuation:TRACe:ACLR:AVERage \n
		Snippet: value: ResultData = driver.multiEval.trace.aclr.average.read() \n
		Returns the absolute powers as displayed in the ACLR diagram. The current and average values can be retrieved. See also
		'Square Spectrum ACLR'. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:LTE:MEASurement<Instance>:MEValuation:TRACe:ACLR:AVERage?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:TRACe:ACLR:AVERage \n
		Snippet: value: ResultData = driver.multiEval.trace.aclr.average.fetch() \n
		Returns the absolute powers as displayed in the ACLR diagram. The current and average values can be retrieved. See also
		'Square Spectrum ACLR'. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:LTE:MEASurement<Instance>:MEValuation:TRACe:ACLR:AVERage?', self.__class__.ResultData())

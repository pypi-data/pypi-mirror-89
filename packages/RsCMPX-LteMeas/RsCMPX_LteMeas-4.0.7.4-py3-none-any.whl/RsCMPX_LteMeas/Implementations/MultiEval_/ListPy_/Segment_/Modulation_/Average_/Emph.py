from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Emph:
	"""Emph commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("emph", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: No parameter help available
			- Evm_Rms_Low: float: No parameter help available
			- Evm_Rms_High: float: No parameter help available
			- Evmpeak_Low: float: No parameter help available
			- Evmpeak_High: float: No parameter help available
			- Mag_Error_Rms_Low: float: No parameter help available
			- Mag_Error_Rms_High: float: No parameter help available
			- Mag_Error_Peak_Low: float: No parameter help available
			- Mag_Err_Peak_High: float: No parameter help available
			- Ph_Error_Rms_Low: float: No parameter help available
			- Ph_Error_Rms_High: float: No parameter help available
			- Ph_Error_Peak_Low: float: No parameter help available
			- Ph_Error_Peak_High: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Evm_Rms_Low'),
			ArgStruct.scalar_float('Evm_Rms_High'),
			ArgStruct.scalar_float('Evmpeak_Low'),
			ArgStruct.scalar_float('Evmpeak_High'),
			ArgStruct.scalar_float('Mag_Error_Rms_Low'),
			ArgStruct.scalar_float('Mag_Error_Rms_High'),
			ArgStruct.scalar_float('Mag_Error_Peak_Low'),
			ArgStruct.scalar_float('Mag_Err_Peak_High'),
			ArgStruct.scalar_float('Ph_Error_Rms_Low'),
			ArgStruct.scalar_float('Ph_Error_Rms_High'),
			ArgStruct.scalar_float('Ph_Error_Peak_Low'),
			ArgStruct.scalar_float('Ph_Error_Peak_High')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Evm_Rms_Low: float = None
			self.Evm_Rms_High: float = None
			self.Evmpeak_Low: float = None
			self.Evmpeak_High: float = None
			self.Mag_Error_Rms_Low: float = None
			self.Mag_Error_Rms_High: float = None
			self.Mag_Error_Peak_Low: float = None
			self.Mag_Err_Peak_High: float = None
			self.Ph_Error_Rms_Low: float = None
			self.Ph_Error_Rms_High: float = None
			self.Ph_Error_Peak_Low: float = None
			self.Ph_Error_Peak_High: float = None

	def fetch(self, segment=repcap.Segment.Default) -> FetchStruct:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>:MODulation:AVERage:EMPH \n
		Snippet: value: FetchStruct = driver.multiEval.listPy.segment.modulation.average.emph.fetch(segment = repcap.Segment.Default) \n
		No command help available \n
			:param segment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		return self._core.io.query_struct(f'FETCh:LTE:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:MODulation:AVERage:EMPH?', self.__class__.FetchStruct())

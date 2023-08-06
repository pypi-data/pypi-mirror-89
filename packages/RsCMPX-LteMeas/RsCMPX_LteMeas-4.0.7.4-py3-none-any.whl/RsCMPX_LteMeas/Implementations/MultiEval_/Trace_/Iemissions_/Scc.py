from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Scc:
	"""Scc commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scc", core, parent)

	def read(self) -> List[float]:
		"""SCPI: READ:LTE:MEASurement<Instance>:MEValuation:TRACe:IEMissions:SCC \n
		Snippet: value: List[float] = driver.multiEval.trace.iemissions.scc.read() \n
		No command help available \n
		Suppressed linked return values: reliability \n
			:return: power: No help available"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:LTE:MEASurement<Instance>:MEValuation:TRACe:IEMissions:SCC?', suppressed)
		return response

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:TRACe:IEMissions:SCC \n
		Snippet: value: List[float] = driver.multiEval.trace.iemissions.scc.fetch() \n
		No command help available \n
		Suppressed linked return values: reliability \n
			:return: power: No help available"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:LTE:MEASurement<Instance>:MEValuation:TRACe:IEMissions:SCC?', suppressed)
		return response

from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("current", core, parent)

	def read(self) -> List[float]:
		"""SCPI: READ:LTE:MEASurement<Instance>:PRACh:TRACe:PDYNamics:CURRent \n
		Snippet: value: List[float] = driver.prach.trace.pdynamics.current.read() \n
		Return the values of the power dynamics traces. Each value is sampled with 48 Ts, corresponding to 1.5625 µs. The results
		of the current, average and maximum traces can be retrieved. See also 'Square Power Dynamics'. \n
		Suppressed linked return values: reliability \n
			:return: power: 2048 power values, from -1100 µs to +2098.4375 µs relative to the start of the preamble. The values have a spacing of 1.5625 µs. The 705th value is at the start of the preamble (0 µs) ."""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:LTE:MEASurement<Instance>:PRACh:TRACe:PDYNamics:CURRent?', suppressed)
		return response

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:PRACh:TRACe:PDYNamics:CURRent \n
		Snippet: value: List[float] = driver.prach.trace.pdynamics.current.fetch() \n
		Return the values of the power dynamics traces. Each value is sampled with 48 Ts, corresponding to 1.5625 µs. The results
		of the current, average and maximum traces can be retrieved. See also 'Square Power Dynamics'. \n
		Suppressed linked return values: reliability \n
			:return: power: 2048 power values, from -1100 µs to +2098.4375 µs relative to the start of the preamble. The values have a spacing of 1.5625 µs. The 705th value is at the start of the preamble (0 µs) ."""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:LTE:MEASurement<Instance>:PRACh:TRACe:PDYNamics:CURRent?', suppressed)
		return response

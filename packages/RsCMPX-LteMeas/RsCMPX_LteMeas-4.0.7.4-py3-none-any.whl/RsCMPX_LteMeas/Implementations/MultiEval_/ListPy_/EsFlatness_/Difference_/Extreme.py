from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Extreme:
	"""Extreme commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("extreme", core, parent)

	def fetch(self, difference=repcap.Difference.Default) -> List[float]:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:LIST:ESFLatness:DIFFerence<nr>:EXTReme \n
		Snippet: value: List[float] = driver.multiEval.listPy.esFlatness.difference.extreme.fetch(difference = repcap.Difference.Default) \n
		Return equalizer spectrum flatness single value results (differences between ranges) for all measured list mode segments.
		The values described below are returned by FETCh commands. CALCulate commands return limit check results instead, one
		value for each result listed below. \n
		Suppressed linked return values: reliability \n
			:param difference: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Difference')
			:return: difference: Comma-separated list of values, one per measured segment"""
		difference_cmd_val = self._base.get_repcap_cmd_value(difference, repcap.Difference)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:LTE:MEASurement<Instance>:MEValuation:LIST:ESFLatness:DIFFerence{difference_cmd_val}:EXTReme?', suppressed)
		return response

	def calculate(self, difference=repcap.Difference.Default) -> List[float]:
		"""SCPI: CALCulate:LTE:MEASurement<Instance>:MEValuation:LIST:ESFLatness:DIFFerence<nr>:EXTReme \n
		Snippet: value: List[float] = driver.multiEval.listPy.esFlatness.difference.extreme.calculate(difference = repcap.Difference.Default) \n
		Return equalizer spectrum flatness single value results (differences between ranges) for all measured list mode segments.
		The values described below are returned by FETCh commands. CALCulate commands return limit check results instead, one
		value for each result listed below. \n
		Suppressed linked return values: reliability \n
			:param difference: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Difference')
			:return: difference: Comma-separated list of values, one per measured segment"""
		difference_cmd_val = self._base.get_repcap_cmd_value(difference, repcap.Difference)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'CALCulate:LTE:MEASurement<Instance>:MEValuation:LIST:ESFLatness:DIFFerence{difference_cmd_val}:EXTReme?', suppressed)
		return response

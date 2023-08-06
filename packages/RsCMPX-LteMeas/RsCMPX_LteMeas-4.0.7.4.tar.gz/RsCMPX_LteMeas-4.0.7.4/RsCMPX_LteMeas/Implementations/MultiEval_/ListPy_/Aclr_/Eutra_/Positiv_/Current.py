from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .......Internal.Types import DataType
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("current", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:LIST:ACLR:EUTRa:POSitiv:CURRent \n
		Snippet: value: List[float] = driver.multiEval.listPy.aclr.eutra.positiv.current.fetch() \n
		Return the ACLR for the first adjacent E-UTRA channel above (POSitiv) or below (NEGativ) the carrier frequency for all
		measured list mode segments. The values described below are returned by FETCh commands. CALCulate commands return limit
		check results instead, one value for each result listed below. \n
		Suppressed linked return values: reliability \n
			:return: eutrapositiv: Comma-separated list of values, one per measured segment"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:LTE:MEASurement<Instance>:MEValuation:LIST:ACLR:EUTRa:POSitiv:CURRent?', suppressed)
		return response

	# noinspection PyTypeChecker
	def calculate(self) -> List[enums.ResultStatus2]:
		"""SCPI: CALCulate:LTE:MEASurement<Instance>:MEValuation:LIST:ACLR:EUTRa:POSitiv:CURRent \n
		Snippet: value: List[enums.ResultStatus2] = driver.multiEval.listPy.aclr.eutra.positiv.current.calculate() \n
		Return the ACLR for the first adjacent E-UTRA channel above (POSitiv) or below (NEGativ) the carrier frequency for all
		measured list mode segments. The values described below are returned by FETCh commands. CALCulate commands return limit
		check results instead, one value for each result listed below. \n
		Suppressed linked return values: reliability \n
			:return: eutrapositiv: Comma-separated list of values, one per measured segment"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'CALCulate:LTE:MEASurement<Instance>:MEValuation:LIST:ACLR:EUTRa:POSitiv:CURRent?', suppressed)
		return Conversions.str_to_list_enum(response, enums.ResultStatus2)

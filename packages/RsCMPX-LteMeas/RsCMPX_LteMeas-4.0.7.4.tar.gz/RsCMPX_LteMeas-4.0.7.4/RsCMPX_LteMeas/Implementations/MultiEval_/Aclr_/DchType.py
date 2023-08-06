from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ....Internal.Types import DataType
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DchType:
	"""DchType commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dchType", core, parent)

	# noinspection PyTypeChecker
	def fetch(self) -> enums.UplinkChannelType:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:ACLR:DCHType \n
		Snippet: value: enums.UplinkChannelType = driver.multiEval.aclr.dchType.fetch() \n
		Returns the uplink channel type for the measured slot. If the same slot is measured by the individual measurements, all
		commands yield the same result. If different statistic counts are defined for the modulation, ACLR and spectrum emission
		mask measurements, different slots can be measured and different results can be returned by the individual commands. \n
		Suppressed linked return values: reliability \n
			:return: channel_type: No help available"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:LTE:MEASurement<Instance>:MEValuation:ACLR:DCHType?', suppressed)
		return Conversions.str_to_scalar_enum(response, enums.UplinkChannelType)

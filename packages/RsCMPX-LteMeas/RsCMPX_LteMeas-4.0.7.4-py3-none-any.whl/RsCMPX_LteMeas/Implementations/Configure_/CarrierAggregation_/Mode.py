from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mode", core, parent)

	# noinspection PyTypeChecker
	def get_combined_signal_path(self) -> enums.CarrAggrMode:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:CAGGregation:MODE:CSPath \n
		Snippet: value: enums.CarrAggrMode = driver.configure.carrierAggregation.mode.get_combined_signal_path() \n
		No command help available \n
			:return: ca_mode: No help available
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:CAGGregation:MODE:CSPath?')
		return Conversions.str_to_scalar_enum(response, enums.CarrAggrMode)

	# noinspection PyTypeChecker
	def get_value(self) -> enums.CarrAggrMode:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:CAGGregation:MODE \n
		Snippet: value: enums.CarrAggrMode = driver.configure.carrierAggregation.mode.get_value() \n
		Selects how many component carriers with intra-band contiguous aggregation are measured. For Signal Path = Network, the
		setting is not configurable. \n
			:return: ca_mode: OFF: only one carrier is measured INTRaband: two carriers (BW class B & C) ICD: three carriers (BW class D) ICE: four carriers (BW class E)
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:CAGGregation:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.CarrAggrMode)

	def set_value(self, ca_mode: enums.CarrAggrMode) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:CAGGregation:MODE \n
		Snippet: driver.configure.carrierAggregation.mode.set_value(ca_mode = enums.CarrAggrMode.ICD) \n
		Selects how many component carriers with intra-band contiguous aggregation are measured. For Signal Path = Network, the
		setting is not configurable. \n
			:param ca_mode: OFF: only one carrier is measured INTRaband: two carriers (BW class B & C) ICD: three carriers (BW class D) ICE: four carriers (BW class E)
		"""
		param = Conversions.enum_scalar_to_str(ca_mode, enums.CarrAggrMode)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:CAGGregation:MODE {param}')

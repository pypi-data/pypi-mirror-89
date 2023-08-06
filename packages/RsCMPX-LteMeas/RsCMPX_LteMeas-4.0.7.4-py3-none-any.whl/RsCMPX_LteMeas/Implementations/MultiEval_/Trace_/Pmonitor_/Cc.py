from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cc:
	"""Cc commands group definition. 2 total commands, 0 Sub-groups, 2 group commands
	Repeated Capability: CarrierComponent, default value after init: CarrierComponent.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cc", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_carrierComponent_get', 'repcap_carrierComponent_set', repcap.CarrierComponent.Nr1)

	def repcap_carrierComponent_set(self, enum_value: repcap.CarrierComponent) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to CarrierComponent.Default
		Default value after init: CarrierComponent.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_carrierComponent_get(self) -> repcap.CarrierComponent:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def read(self, carrierComponent=repcap.CarrierComponent.Default) -> List[float]:
		"""SCPI: READ:LTE:MEASurement<Instance>:MEValuation:TRACe:PMONitor:CC<Nr> \n
		Snippet: value: List[float] = driver.multiEval.trace.pmonitor.cc.read(carrierComponent = repcap.CarrierComponent.Default) \n
		Returns the power monitor results for all captured CC<no> subframes. \n
		Suppressed linked return values: reliability \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: power: Comma-separated list of power values, one value per subframe"""
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:LTE:MEASurement<Instance>:MEValuation:TRACe:PMONitor:CC{carrierComponent_cmd_val}?', suppressed)
		return response

	def fetch(self, carrierComponent=repcap.CarrierComponent.Default) -> List[float]:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:TRACe:PMONitor:CC<Nr> \n
		Snippet: value: List[float] = driver.multiEval.trace.pmonitor.cc.fetch(carrierComponent = repcap.CarrierComponent.Default) \n
		Returns the power monitor results for all captured CC<no> subframes. \n
		Suppressed linked return values: reliability \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: power: Comma-separated list of power values, one value per subframe"""
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:LTE:MEASurement<Instance>:MEValuation:TRACe:PMONitor:CC{carrierComponent_cmd_val}?', suppressed)
		return response

	def clone(self) -> 'Cc':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Cc(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

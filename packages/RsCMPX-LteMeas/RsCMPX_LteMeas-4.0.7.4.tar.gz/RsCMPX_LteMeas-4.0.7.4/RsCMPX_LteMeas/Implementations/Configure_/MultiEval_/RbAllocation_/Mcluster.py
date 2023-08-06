from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mcluster:
	"""Mcluster commands group definition. 3 total commands, 2 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mcluster", core, parent)

	@property
	def nrb(self):
		"""nrb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nrb'):
			from .Mcluster_.Nrb import Nrb
			self._nrb = Nrb(self._core, self._base)
		return self._nrb

	@property
	def orb(self):
		"""orb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_orb'):
			from .Mcluster_.Orb import Orb
			self._orb = Orb(self._core, self._base)
		return self._orb

	def get_value(self) -> bool:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:RBALlocation:MCLuster \n
		Snippet: value: bool = driver.configure.multiEval.rbAllocation.mcluster.get_value() \n
		Specifies whether the UL signal uses multi-cluster allocation or not. \n
			:return: enable: OFF: contiguous allocation, resource allocation type 0 ON: multi-cluster allocation, resource allocation type 1
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:MEValuation:RBALlocation:MCLuster?')
		return Conversions.str_to_bool(response)

	def set_value(self, enable: bool) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:RBALlocation:MCLuster \n
		Snippet: driver.configure.multiEval.rbAllocation.mcluster.set_value(enable = False) \n
		Specifies whether the UL signal uses multi-cluster allocation or not. \n
			:param enable: OFF: contiguous allocation, resource allocation type 0 ON: multi-cluster allocation, resource allocation type 1
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:RBALlocation:MCLuster {param}')

	def clone(self) -> 'Mcluster':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Mcluster(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

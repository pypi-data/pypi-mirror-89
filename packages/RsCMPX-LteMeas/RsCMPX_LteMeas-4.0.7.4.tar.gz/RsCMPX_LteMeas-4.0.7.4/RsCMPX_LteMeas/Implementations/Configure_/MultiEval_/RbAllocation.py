from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RbAllocation:
	"""RbAllocation commands group definition. 10 total commands, 3 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rbAllocation", core, parent)

	@property
	def nrb(self):
		"""nrb commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_nrb'):
			from .RbAllocation_.Nrb import Nrb
			self._nrb = Nrb(self._core, self._base)
		return self._nrb

	@property
	def mcluster(self):
		"""mcluster commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcluster'):
			from .RbAllocation_.Mcluster import Mcluster
			self._mcluster = Mcluster(self._core, self._base)
		return self._mcluster

	@property
	def orb(self):
		"""orb commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_orb'):
			from .RbAllocation_.Orb import Orb
			self._orb = Orb(self._core, self._base)
		return self._orb

	def get_auto(self) -> bool:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:RBALlocation:AUTO \n
		Snippet: value: bool = driver.configure.multiEval.rbAllocation.get_auto() \n
		Enables or disables the automatic detection of the RB configuration. \n
			:return: auto: OFF: manual definition ON: automatic detection
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:MEValuation:RBALlocation:AUTO?')
		return Conversions.str_to_bool(response)

	def set_auto(self, auto: bool) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:RBALlocation:AUTO \n
		Snippet: driver.configure.multiEval.rbAllocation.set_auto(auto = False) \n
		Enables or disables the automatic detection of the RB configuration. \n
			:param auto: OFF: manual definition ON: automatic detection
		"""
		param = Conversions.bool_to_str(auto)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:RBALlocation:AUTO {param}')

	def clone(self) -> 'RbAllocation':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RbAllocation(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

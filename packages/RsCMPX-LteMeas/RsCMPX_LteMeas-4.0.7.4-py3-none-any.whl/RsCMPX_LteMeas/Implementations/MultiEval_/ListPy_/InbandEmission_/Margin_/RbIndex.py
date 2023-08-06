from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RbIndex:
	"""RbIndex commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rbIndex", core, parent)

	@property
	def current(self):
		"""current commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_current'):
			from .RbIndex_.Current import Current
			self._current = Current(self._core, self._base)
		return self._current

	@property
	def extreme(self):
		"""extreme commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_extreme'):
			from .RbIndex_.Extreme import Extreme
			self._extreme = Extreme(self._core, self._base)
		return self._extreme

	def clone(self) -> 'RbIndex':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RbIndex(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ulca:
	"""Ulca commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ulca", core, parent)

	@property
	def scc(self):
		"""scc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scc'):
			from .Ulca_.Scc import Scc
			self._scc = Scc(self._core, self._base)
		return self._scc

	def get_pcc(self) -> List[float]:
		"""SCPI: SENSe:LTE:MEASurement<Instance>:MEValuation:LIMit:IEMissions:ULCA[:PCC] \n
		Snippet: value: List[float] = driver.sense.multiEval.limit.iemissions.ulca.get_pcc() \n
		No command help available \n
			:return: power: No help available
		"""
		response = self._core.io.query_bin_or_ascii_float_list('SENSe:LTE:MEASurement<Instance>:MEValuation:LIMit:IEMissions:ULCA:PCC?')
		return response

	def clone(self) -> 'Ulca':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ulca(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

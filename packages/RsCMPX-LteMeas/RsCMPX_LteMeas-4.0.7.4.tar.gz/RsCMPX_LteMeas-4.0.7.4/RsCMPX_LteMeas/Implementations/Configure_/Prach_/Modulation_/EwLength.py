from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EwLength:
	"""EwLength commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ewLength", core, parent)

	@property
	def pformat(self):
		"""pformat commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pformat'):
			from .EwLength_.Pformat import Pformat
			self._pformat = Pformat(self._core, self._base)
		return self._pformat

	def get_value(self) -> List[int]:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:PRACh:MODulation:EWLength \n
		Snippet: value: List[int] = driver.configure.prach.modulation.ewLength.get_value() \n
		Specifies the EVM window length in samples for all preamble formats. \n
			:return: evmwindow_length: No help available
		"""
		response = self._core.io.query_bin_or_ascii_int_list('CONFigure:LTE:MEASurement<Instance>:PRACh:MODulation:EWLength?')
		return response

	def set_value(self, evmwindow_length: List[int]) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:PRACh:MODulation:EWLength \n
		Snippet: driver.configure.prach.modulation.ewLength.set_value(evmwindow_length = [1, 2, 3]) \n
		Specifies the EVM window length in samples for all preamble formats. \n
			:param evmwindow_length: No help available
		"""
		param = Conversions.list_to_csv_str(evmwindow_length)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:PRACh:MODulation:EWLength {param}')

	def clone(self) -> 'EwLength':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = EwLength(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

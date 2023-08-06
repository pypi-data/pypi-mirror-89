from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SingleCmw:
	"""SingleCmw commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("singleCmw", core, parent)

	@property
	def connector(self):
		"""connector commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_connector'):
			from .SingleCmw_.Connector import Connector
			self._connector = Connector(self._core, self._base)
		return self._connector

	# noinspection PyTypeChecker
	def get_cmode(self) -> enums.ParameterSetMode:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:LIST:CMWS:CMODe \n
		Snippet: value: enums.ParameterSetMode = driver.configure.multiEval.listPy.singleCmw.get_cmode() \n
		No command help available \n
			:return: connector_mode: No help available
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:MEValuation:LIST:CMWS:CMODe?')
		return Conversions.str_to_scalar_enum(response, enums.ParameterSetMode)

	def set_cmode(self, connector_mode: enums.ParameterSetMode) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:LIST:CMWS:CMODe \n
		Snippet: driver.configure.multiEval.listPy.singleCmw.set_cmode(connector_mode = enums.ParameterSetMode.GLOBal) \n
		No command help available \n
			:param connector_mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(connector_mode, enums.ParameterSetMode)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:LIST:CMWS:CMODe {param}')

	def clone(self) -> 'SingleCmw':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SingleCmw(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

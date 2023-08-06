from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.Types import DataType
from .........Internal.ArgSingleList import ArgSingleList
from .........Internal.ArgSingle import ArgSingle
from ......... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pattern:
	"""Pattern commands group definition. 3 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pattern", core, parent)

	@property
	def userDefined(self):
		"""userDefined commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_userDefined'):
			from .Pattern_.UserDefined import UserDefined
			self._userDefined = UserDefined(self._core, self._base)
		return self._userDefined

	def set(self, cell_name: str, type_py: enums.TypeB) -> None:
		"""SCPI: [CONFigure]:SIGNaling:LTE:CELL:POWer:CONTrol:TPControl:PATTern \n
		Snippet: driver.configure.signaling.lte.cell.power.control.tpControl.pattern.set(cell_name = '1', type_py = enums.TypeB.UDEFined) \n
		No command help available \n
			:param cell_name: No help available
			:param type_py: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cell_name', cell_name, DataType.String), ArgSingle('type_py', type_py, DataType.Enum))
		self._core.io.write(f'CONFigure:SIGNaling:LTE:CELL:POWer:CONTrol:TPControl:PATTern {param}'.rstrip())

	# noinspection PyTypeChecker
	def get(self, cell_name: str) -> enums.TypeB:
		"""SCPI: [CONFigure]:SIGNaling:LTE:CELL:POWer:CONTrol:TPControl:PATTern \n
		Snippet: value: enums.TypeB = driver.configure.signaling.lte.cell.power.control.tpControl.pattern.get(cell_name = '1') \n
		No command help available \n
			:param cell_name: No help available
			:return: type_py: No help available"""
		param = Conversions.value_to_quoted_str(cell_name)
		response = self._core.io.query_str(f'CONFigure:SIGNaling:LTE:CELL:POWer:CONTrol:TPControl:PATTern? {param}')
		return Conversions.str_to_scalar_enum(response, enums.TypeB)

	def clone(self) -> 'Pattern':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Pattern(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Lte:
	"""Lte commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lte", core, parent)

	@property
	def cell(self):
		"""cell commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cell'):
			from .Lte_.Cell import Cell
			self._cell = Cell(self._core, self._base)
		return self._cell

	def set_cgroup(self, cell_group_name: str) -> None:
		"""SCPI: CREate:SIGNaling:LTE:CGRoup \n
		Snippet: driver.create.signaling.lte.set_cgroup(cell_group_name = '1') \n
		Creates an LTE or NR cell group. \n
			:param cell_group_name: Assigns a name to the cell group. The string is used in other commands to select this cell group.
		"""
		param = Conversions.value_to_quoted_str(cell_group_name)
		self._core.io.write(f'CREate:SIGNaling:LTE:CGRoup {param}')

	def clone(self) -> 'Lte':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Lte(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

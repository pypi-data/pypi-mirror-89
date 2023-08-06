from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tdd:
	"""Tdd commands group definition. 6 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tdd", core, parent)

	@property
	def pattern(self):
		"""pattern commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_pattern'):
			from .Tdd_.Pattern import Pattern
			self._pattern = Pattern(self._core, self._base)
		return self._pattern

	def clone(self) -> 'Tdd':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tdd(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

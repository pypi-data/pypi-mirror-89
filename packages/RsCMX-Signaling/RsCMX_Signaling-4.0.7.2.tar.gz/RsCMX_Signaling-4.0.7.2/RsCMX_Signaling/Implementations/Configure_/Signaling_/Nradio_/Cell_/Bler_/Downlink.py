from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Downlink:
	"""Downlink commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("downlink", core, parent)

	@property
	def percent(self):
		"""percent commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_percent'):
			from .Downlink_.Percent import Percent
			self._percent = Percent(self._core, self._base)
		return self._percent

	@property
	def thousandth(self):
		"""thousandth commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_thousandth'):
			from .Downlink_.Thousandth import Thousandth
			self._thousandth = Thousandth(self._core, self._base)
		return self._thousandth

	def clone(self) -> 'Downlink':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Downlink(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Scell:
	"""Scell commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scell", core, parent)

	def set(self, cell_group_name: str, cell_name: str) -> None:
		"""SCPI: REMove:SIGNaling:LTE:CA:SCELl \n
		Snippet: driver.remove.signaling.lte.ca.scell.set(cell_group_name = '1', cell_name = '1') \n
		Removes an LTE or NR cell from a cell group. \n
			:param cell_group_name: No help available
			:param cell_name: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cell_group_name', cell_group_name, DataType.String), ArgSingle('cell_name', cell_name, DataType.String))
		self._core.io.write(f'REMove:SIGNaling:LTE:CA:SCELl {param}'.rstrip())

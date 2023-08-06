from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cell:
	"""Cell commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cell", core, parent)

	def set(self, cell_name: str, physical_cell_id: float = None) -> None:
		"""SCPI: CREate:SIGNaling:NRADio:CELL \n
		Snippet: driver.create.signaling.nradio.cell.set(cell_name = '1', physical_cell_id = 1.0) \n
		Creates an NR cell. \n
			:param cell_name: Assigns a name to the cell. The string is used in other commands to select this cell.
			:param physical_cell_id: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cell_name', cell_name, DataType.String), ArgSingle('physical_cell_id', physical_cell_id, DataType.Float, True))
		self._core.io.write(f'CREate:SIGNaling:NRADio:CELL {param}'.rstrip())

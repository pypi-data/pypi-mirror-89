from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Types import DataType
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle
from ........ import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Assignment:
	"""Assignment commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("assignment", core, parent)

	def set(self, cell_name: str, assignment: enums.Assignment) -> None:
		"""SCPI: [CONFigure]:SIGNaling:LTE:CELL:TDD:SUBFrame:ASSignment \n
		Snippet: driver.configure.signaling.lte.cell.tdd.subframe.assignment.set(cell_name = '1', assignment = enums.Assignment.NONE) \n
		Selects the subframe assignment, defining the combination of UL, DL and special subframes within a TDD radio frame. \n
			:param cell_name: No help available
			:param assignment: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cell_name', cell_name, DataType.String), ArgSingle('assignment', assignment, DataType.Enum))
		self._core.io.write(f'CONFigure:SIGNaling:LTE:CELL:TDD:SUBFrame:ASSignment {param}'.rstrip())

	# noinspection PyTypeChecker
	def get(self, cell_name: str) -> enums.Assignment:
		"""SCPI: [CONFigure]:SIGNaling:LTE:CELL:TDD:SUBFrame:ASSignment \n
		Snippet: value: enums.Assignment = driver.configure.signaling.lte.cell.tdd.subframe.assignment.get(cell_name = '1') \n
		Selects the subframe assignment, defining the combination of UL, DL and special subframes within a TDD radio frame. \n
			:param cell_name: No help available
			:return: assignment: No help available"""
		param = Conversions.value_to_quoted_str(cell_name)
		response = self._core.io.query_str(f'CONFigure:SIGNaling:LTE:CELL:TDD:SUBFrame:ASSignment? {param}')
		return Conversions.str_to_scalar_enum(response, enums.Assignment)

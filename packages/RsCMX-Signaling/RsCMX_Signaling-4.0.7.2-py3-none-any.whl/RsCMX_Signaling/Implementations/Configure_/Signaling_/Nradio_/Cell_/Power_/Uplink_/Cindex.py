from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Types import DataType
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cindex:
	"""Cindex commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cindex", core, parent)

	def set(self, cell_name: str, index: int) -> None:
		"""SCPI: [CONFigure]:SIGNaling:NRADio:CELL:POWer:UL:CINDex \n
		Snippet: driver.configure.signaling.nradio.cell.power.uplink.cindex.set(cell_name = '1', index = 1) \n
		No command help available \n
			:param cell_name: No help available
			:param index: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cell_name', cell_name, DataType.String), ArgSingle('index', index, DataType.Integer))
		self._core.io.write(f'CONFigure:SIGNaling:NRADio:CELL:POWer:UL:CINDex {param}'.rstrip())

	def get(self, cell_name: str) -> int:
		"""SCPI: [CONFigure]:SIGNaling:NRADio:CELL:POWer:UL:CINDex \n
		Snippet: value: int = driver.configure.signaling.nradio.cell.power.uplink.cindex.get(cell_name = '1') \n
		No command help available \n
			:param cell_name: No help available
			:return: index: No help available"""
		param = Conversions.value_to_quoted_str(cell_name)
		response = self._core.io.query_str(f'CONFigure:SIGNaling:NRADio:CELL:POWer:UL:CINDex? {param}')
		return Conversions.str_to_int(response)

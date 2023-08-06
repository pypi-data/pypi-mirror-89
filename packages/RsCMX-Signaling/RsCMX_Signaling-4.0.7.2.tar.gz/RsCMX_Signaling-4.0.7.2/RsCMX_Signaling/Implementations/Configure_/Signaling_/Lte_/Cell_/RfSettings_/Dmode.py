from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Types import DataType
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dmode:
	"""Dmode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dmode", core, parent)

	def set(self, cell_name: str, duplex_mode: enums.DuplexModeB) -> None:
		"""SCPI: [CONFigure]:SIGNaling:LTE:CELL:RFSettings:DMODe \n
		Snippet: driver.configure.signaling.lte.cell.rfSettings.dmode.set(cell_name = '1', duplex_mode = enums.DuplexModeB.FDD) \n
		Selects the duplex mode. \n
			:param cell_name: No help available
			:param duplex_mode: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cell_name', cell_name, DataType.String), ArgSingle('duplex_mode', duplex_mode, DataType.Enum))
		self._core.io.write(f'CONFigure:SIGNaling:LTE:CELL:RFSettings:DMODe {param}'.rstrip())

	# noinspection PyTypeChecker
	def get(self, cell_name: str) -> enums.DuplexModeB:
		"""SCPI: [CONFigure]:SIGNaling:LTE:CELL:RFSettings:DMODe \n
		Snippet: value: enums.DuplexModeB = driver.configure.signaling.lte.cell.rfSettings.dmode.get(cell_name = '1') \n
		Selects the duplex mode. \n
			:param cell_name: No help available
			:return: duplex_mode: No help available"""
		param = Conversions.value_to_quoted_str(cell_name)
		response = self._core.io.query_str(f'CONFigure:SIGNaling:LTE:CELL:RFSettings:DMODe? {param}')
		return Conversions.str_to_scalar_enum(response, enums.DuplexModeB)

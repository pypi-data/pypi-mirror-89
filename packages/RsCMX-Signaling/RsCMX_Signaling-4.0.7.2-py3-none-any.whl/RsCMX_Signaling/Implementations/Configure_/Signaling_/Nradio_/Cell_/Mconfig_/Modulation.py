from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Types import DataType
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Modulation:
	"""Modulation commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("modulation", core, parent)

	def set(self, cell_name: str, modulation: enums.Modulation) -> None:
		"""SCPI: [CONFigure]:SIGNaling:NRADio:CELL:MCONfig:MODulation \n
		Snippet: driver.configure.signaling.nradio.cell.mconfig.modulation.set(cell_name = '1', modulation = enums.Modulation.BPSK) \n
		Selects the maximum UL modulation type allowed in live mode. \n
			:param cell_name: No help available
			:param modulation: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cell_name', cell_name, DataType.String), ArgSingle('modulation', modulation, DataType.Enum))
		self._core.io.write(f'CONFigure:SIGNaling:NRADio:CELL:MCONfig:MODulation {param}'.rstrip())

	# noinspection PyTypeChecker
	def get(self, cell_name: str) -> enums.Modulation:
		"""SCPI: [CONFigure]:SIGNaling:NRADio:CELL:MCONfig:MODulation \n
		Snippet: value: enums.Modulation = driver.configure.signaling.nradio.cell.mconfig.modulation.get(cell_name = '1') \n
		Selects the maximum UL modulation type allowed in live mode. \n
			:param cell_name: No help available
			:return: modulation: No help available"""
		param = Conversions.value_to_quoted_str(cell_name)
		response = self._core.io.query_str(f'CONFigure:SIGNaling:NRADio:CELL:MCONfig:MODulation? {param}')
		return Conversions.str_to_scalar_enum(response, enums.Modulation)

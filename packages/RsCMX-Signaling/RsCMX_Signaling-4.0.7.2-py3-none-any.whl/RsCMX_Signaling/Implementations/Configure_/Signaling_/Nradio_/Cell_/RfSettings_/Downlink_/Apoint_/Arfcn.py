from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.Types import DataType
from .........Internal.ArgSingleList import ArgSingleList
from .........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Arfcn:
	"""Arfcn commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("arfcn", core, parent)

	def set(self, cell_name: str, number: int) -> None:
		"""SCPI: [CONFigure]:SIGNaling:NRADio:CELL:RFSettings:DL:APOint:ARFCn \n
		Snippet: driver.configure.signaling.nradio.cell.rfSettings.downlink.apoint.arfcn.set(cell_name = '1', number = 1) \n
		Sets the user-defined channel number of point A, for the downlink. \n
			:param cell_name: No help available
			:param number: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cell_name', cell_name, DataType.String), ArgSingle('number', number, DataType.Integer))
		self._core.io.write(f'CONFigure:SIGNaling:NRADio:CELL:RFSettings:DL:APOint:ARFCn {param}'.rstrip())

	def get(self, cell_name: str) -> int:
		"""SCPI: [CONFigure]:SIGNaling:NRADio:CELL:RFSettings:DL:APOint:ARFCn \n
		Snippet: value: int = driver.configure.signaling.nradio.cell.rfSettings.downlink.apoint.arfcn.get(cell_name = '1') \n
		Sets the user-defined channel number of point A, for the downlink. \n
			:param cell_name: No help available
			:return: number: No help available"""
		param = Conversions.value_to_quoted_str(cell_name)
		response = self._core.io.query_str(f'CONFigure:SIGNaling:NRADio:CELL:RFSettings:DL:APOint:ARFCn? {param}')
		return Conversions.str_to_int(response)

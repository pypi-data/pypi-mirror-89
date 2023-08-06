from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ssid:
	"""Ssid commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ssid", core, parent)

	def get(self, cell_name: str) -> int:
		"""SCPI: [CONFigure]:SIGNaling:NRADio:CELL:UESCheduling:UDEFined:DL:SSID \n
		Snippet: value: int = driver.configure.signaling.nradio.cell.ueScheduling.userDefined.downlink.ssid.get(cell_name = '1') \n
		Queries the ID of the search space, for the DL and user-defined scheduling. \n
			:param cell_name: No help available
			:return: idn: No help available"""
		param = Conversions.value_to_quoted_str(cell_name)
		response = self._core.io.query_str(f'CONFigure:SIGNaling:NRADio:CELL:UESCheduling:UDEFined:DL:SSID? {param}')
		return Conversions.str_to_int(response)

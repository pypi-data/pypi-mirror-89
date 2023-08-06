from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.Types import DataType
from .........Internal.ArgSingleList import ArgSingleList
from .........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Enable:
	"""Enable commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("enable", core, parent)

	def set(self, cell_name: str, enable: bool) -> None:
		"""SCPI: [CONFigure]:SIGNaling:NRADio:CELL:POWer:DL:OCNG:ENABle \n
		Snippet: driver.configure.signaling.nradio.cell.power.downlink.ocng.enable.set(cell_name = '1', enable = False) \n
		Enables or disables the OFDMA channel noise generator (OCNG) . \n
			:param cell_name: No help available
			:param enable: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cell_name', cell_name, DataType.String), ArgSingle('enable', enable, DataType.Boolean))
		self._core.io.write(f'CONFigure:SIGNaling:NRADio:CELL:POWer:DL:OCNG:ENABle {param}'.rstrip())

	def get(self, cell_name: str) -> bool:
		"""SCPI: [CONFigure]:SIGNaling:NRADio:CELL:POWer:DL:OCNG:ENABle \n
		Snippet: value: bool = driver.configure.signaling.nradio.cell.power.downlink.ocng.enable.get(cell_name = '1') \n
		Enables or disables the OFDMA channel noise generator (OCNG) . \n
			:param cell_name: No help available
			:return: enable: No help available"""
		param = Conversions.value_to_quoted_str(cell_name)
		response = self._core.io.query_str(f'CONFigure:SIGNaling:NRADio:CELL:POWer:DL:OCNG:ENABle? {param}')
		return Conversions.str_to_bool(response)

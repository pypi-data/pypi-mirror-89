from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Types import DataType
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PibPsk:
	"""PibPsk commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pibPsk", core, parent)

	def set(self, cell_name: str, enable: bool) -> None:
		"""SCPI: [CONFigure]:SIGNaling:NRADio:CELL:PUSCh:DTFS:PIBPsk \n
		Snippet: driver.configure.signaling.nradio.cell.pusch.dtfs.pibPsk.set(cell_name = '1', enable = False) \n
		Enables the modulation scheme π/2-BPSK for PUSCH with transform precoding. \n
			:param cell_name: No help available
			:param enable: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cell_name', cell_name, DataType.String), ArgSingle('enable', enable, DataType.Boolean))
		self._core.io.write(f'CONFigure:SIGNaling:NRADio:CELL:PUSCh:DTFS:PIBPsk {param}'.rstrip())

	def get(self, cell_name: str) -> bool:
		"""SCPI: [CONFigure]:SIGNaling:NRADio:CELL:PUSCh:DTFS:PIBPsk \n
		Snippet: value: bool = driver.configure.signaling.nradio.cell.pusch.dtfs.pibPsk.get(cell_name = '1') \n
		Enables the modulation scheme π/2-BPSK for PUSCH with transform precoding. \n
			:param cell_name: No help available
			:return: enable: No help available"""
		param = Conversions.value_to_quoted_str(cell_name)
		response = self._core.io.query_str(f'CONFigure:SIGNaling:NRADio:CELL:PUSCh:DTFS:PIBPsk? {param}')
		return Conversions.str_to_bool(response)

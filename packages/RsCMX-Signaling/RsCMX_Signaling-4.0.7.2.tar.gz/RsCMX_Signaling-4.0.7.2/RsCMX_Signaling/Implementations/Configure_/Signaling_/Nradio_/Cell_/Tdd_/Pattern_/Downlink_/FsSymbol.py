from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.Types import DataType
from .........Internal.ArgSingleList import ArgSingleList
from .........Internal.ArgSingle import ArgSingle
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FsSymbol:
	"""FsSymbol commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fsSymbol", core, parent)

	def set(self, cell_name: str, symbol: int, pattern=repcap.Pattern.Default) -> None:
		"""SCPI: [CONFigure]:SIGNaling:NRADio:CELL:TDD:PATTern<PatternNr>:DL:FSSYmbol \n
		Snippet: driver.configure.signaling.nradio.cell.tdd.pattern.downlink.fsSymbol.set(cell_name = '1', symbol = 1, pattern = repcap.Pattern.Default) \n
		Defines the number of DL symbols in the flexible slot of the UL-DL pattern {p}. \n
			:param cell_name: No help available
			:param symbol: No help available
			:param pattern: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Pattern')"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cell_name', cell_name, DataType.String), ArgSingle('symbol', symbol, DataType.Integer))
		pattern_cmd_val = self._base.get_repcap_cmd_value(pattern, repcap.Pattern)
		self._core.io.write(f'CONFigure:SIGNaling:NRADio:CELL:TDD:PATTern{pattern_cmd_val}:DL:FSSYmbol {param}'.rstrip())

	def get(self, cell_name: str, pattern=repcap.Pattern.Default) -> int:
		"""SCPI: [CONFigure]:SIGNaling:NRADio:CELL:TDD:PATTern<PatternNr>:DL:FSSYmbol \n
		Snippet: value: int = driver.configure.signaling.nradio.cell.tdd.pattern.downlink.fsSymbol.get(cell_name = '1', pattern = repcap.Pattern.Default) \n
		Defines the number of DL symbols in the flexible slot of the UL-DL pattern {p}. \n
			:param cell_name: No help available
			:param pattern: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Pattern')
			:return: symbol: No help available"""
		param = Conversions.value_to_quoted_str(cell_name)
		pattern_cmd_val = self._base.get_repcap_cmd_value(pattern, repcap.Pattern)
		response = self._core.io.query_str(f'CONFigure:SIGNaling:NRADio:CELL:TDD:PATTern{pattern_cmd_val}:DL:FSSYmbol? {param}')
		return Conversions.str_to_int(response)

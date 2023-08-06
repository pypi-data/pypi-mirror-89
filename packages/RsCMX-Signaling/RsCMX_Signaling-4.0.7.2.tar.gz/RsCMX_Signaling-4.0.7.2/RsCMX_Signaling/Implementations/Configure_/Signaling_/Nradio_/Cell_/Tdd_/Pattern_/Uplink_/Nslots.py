from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.Types import DataType
from .........Internal.ArgSingleList import ArgSingleList
from .........Internal.ArgSingle import ArgSingle
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nslots:
	"""Nslots commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nslots", core, parent)

	def set(self, cell_name: str, number: int, pattern=repcap.Pattern.Default) -> None:
		"""SCPI: [CONFigure]:SIGNaling:NRADio:CELL:TDD:PATTern<PatternNr>:UL:NSLots \n
		Snippet: driver.configure.signaling.nradio.cell.tdd.pattern.uplink.nslots.set(cell_name = '1', number = 1, pattern = repcap.Pattern.Default) \n
		Defines the number of UL slots in the UL-DL pattern {p}. \n
			:param cell_name: No help available
			:param number: No help available
			:param pattern: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Pattern')"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cell_name', cell_name, DataType.String), ArgSingle('number', number, DataType.Integer))
		pattern_cmd_val = self._base.get_repcap_cmd_value(pattern, repcap.Pattern)
		self._core.io.write(f'CONFigure:SIGNaling:NRADio:CELL:TDD:PATTern{pattern_cmd_val}:UL:NSLots {param}'.rstrip())

	def get(self, cell_name: str, pattern=repcap.Pattern.Default) -> int:
		"""SCPI: [CONFigure]:SIGNaling:NRADio:CELL:TDD:PATTern<PatternNr>:UL:NSLots \n
		Snippet: value: int = driver.configure.signaling.nradio.cell.tdd.pattern.uplink.nslots.get(cell_name = '1', pattern = repcap.Pattern.Default) \n
		Defines the number of UL slots in the UL-DL pattern {p}. \n
			:param cell_name: No help available
			:param pattern: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Pattern')
			:return: number: No help available"""
		param = Conversions.value_to_quoted_str(cell_name)
		pattern_cmd_val = self._base.get_repcap_cmd_value(pattern, repcap.Pattern)
		response = self._core.io.query_str(f'CONFigure:SIGNaling:NRADio:CELL:TDD:PATTern{pattern_cmd_val}:UL:NSLots? {param}')
		return Conversions.str_to_int(response)

from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from ..........Internal.Types import DataType
from ..........Internal.ArgSingleList import ArgSingleList
from ..........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tpower:
	"""Tpower commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tpower", core, parent)

	def set(self, cell_name: str, power: float) -> None:
		"""SCPI: [CONFigure]:SIGNaling:NRADio:CELL:POWer:CONTrol:TPControl:CLOop:TPOWer \n
		Snippet: driver.configure.signaling.nradio.cell.power.control.tpControl.cloop.tpower.set(cell_name = '1', power = 1.0) \n
		Defines the target power for closed-loop power control. \n
			:param cell_name: No help available
			:param power: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cell_name', cell_name, DataType.String), ArgSingle('power', power, DataType.Float))
		self._core.io.write(f'CONFigure:SIGNaling:NRADio:CELL:POWer:CONTrol:TPControl:CLOop:TPOWer {param}'.rstrip())

	def get(self, cell_name: str) -> float:
		"""SCPI: [CONFigure]:SIGNaling:NRADio:CELL:POWer:CONTrol:TPControl:CLOop:TPOWer \n
		Snippet: value: float = driver.configure.signaling.nradio.cell.power.control.tpControl.cloop.tpower.get(cell_name = '1') \n
		Defines the target power for closed-loop power control. \n
			:param cell_name: No help available
			:return: power: No help available"""
		param = Conversions.value_to_quoted_str(cell_name)
		response = self._core.io.query_str(f'CONFigure:SIGNaling:NRADio:CELL:POWer:CONTrol:TPControl:CLOop:TPOWer? {param}')
		return Conversions.str_to_float(response)

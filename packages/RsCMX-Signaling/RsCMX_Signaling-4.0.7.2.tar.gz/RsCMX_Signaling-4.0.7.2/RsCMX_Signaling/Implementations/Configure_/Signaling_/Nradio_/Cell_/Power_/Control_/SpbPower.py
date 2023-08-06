from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Types import DataType
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SpbPower:
	"""SpbPower commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("spbPower", core, parent)

	def set(self, cell_name: str, power: int) -> None:
		"""SCPI: [CONFigure]:SIGNaling:NRADio:CELL:POWer:CONTrol:SPBPower \n
		Snippet: driver.configure.signaling.nradio.cell.power.control.spbPower.set(cell_name = '1', power = 1) \n
		Defines parameter 'SS-PBCH-BlockPower'. \n
			:param cell_name: No help available
			:param power: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cell_name', cell_name, DataType.String), ArgSingle('power', power, DataType.Integer))
		self._core.io.write(f'CONFigure:SIGNaling:NRADio:CELL:POWer:CONTrol:SPBPower {param}'.rstrip())

	def get(self, cell_name: str) -> int:
		"""SCPI: [CONFigure]:SIGNaling:NRADio:CELL:POWer:CONTrol:SPBPower \n
		Snippet: value: int = driver.configure.signaling.nradio.cell.power.control.spbPower.get(cell_name = '1') \n
		Defines parameter 'SS-PBCH-BlockPower'. \n
			:param cell_name: No help available
			:return: power: No help available"""
		param = Conversions.value_to_quoted_str(cell_name)
		response = self._core.io.query_str(f'CONFigure:SIGNaling:NRADio:CELL:POWer:CONTrol:SPBPower? {param}')
		return Conversions.str_to_int(response)

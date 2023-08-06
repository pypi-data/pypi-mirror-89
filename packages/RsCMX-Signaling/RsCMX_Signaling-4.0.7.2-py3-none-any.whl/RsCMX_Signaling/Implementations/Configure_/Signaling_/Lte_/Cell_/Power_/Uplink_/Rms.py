from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Types import DataType
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rms:
	"""Rms commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rms", core, parent)

	def set(self, cell_name: str, max_exp_rms_pwr: float) -> None:
		"""SCPI: [CONFigure]:SIGNaling:LTE:CELL:POWer:UL:RMS \n
		Snippet: driver.configure.signaling.lte.cell.power.uplink.rms.set(cell_name = '1', max_exp_rms_pwr = 1.0) \n
		Sets the maximum RMS power expected in the UL, for user-defined configuration. \n
			:param cell_name: No help available
			:param max_exp_rms_pwr: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cell_name', cell_name, DataType.String), ArgSingle('max_exp_rms_pwr', max_exp_rms_pwr, DataType.Float))
		self._core.io.write(f'CONFigure:SIGNaling:LTE:CELL:POWer:UL:RMS {param}'.rstrip())

	def get(self, cell_name: str) -> float:
		"""SCPI: [CONFigure]:SIGNaling:LTE:CELL:POWer:UL:RMS \n
		Snippet: value: float = driver.configure.signaling.lte.cell.power.uplink.rms.get(cell_name = '1') \n
		Sets the maximum RMS power expected in the UL, for user-defined configuration. \n
			:param cell_name: No help available
			:return: max_exp_rms_pwr: No help available"""
		param = Conversions.value_to_quoted_str(cell_name)
		response = self._core.io.query_str(f'CONFigure:SIGNaling:LTE:CELL:POWer:UL:RMS? {param}')
		return Conversions.str_to_float(response)

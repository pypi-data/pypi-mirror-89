from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.Types import DataType
from .........Internal.ArgSingleList import ArgSingleList
from .........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ue:
	"""Ue commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ue", core, parent)

	def set(self, cell_name: str, p_0_ue_pusch: float) -> None:
		"""SCPI: [CONFigure]:SIGNaling:LTE:CELL:POWer:UL:PUSCh:UE \n
		Snippet: driver.configure.signaling.lte.cell.power.uplink.pusch.ue.set(cell_name = '1', p_0_ue_pusch = 1.0) \n
		Sets the UL power control parameter 'p0-UE-PUSCH'. \n
			:param cell_name: No help available
			:param p_0_ue_pusch: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cell_name', cell_name, DataType.String), ArgSingle('p_0_ue_pusch', p_0_ue_pusch, DataType.Float))
		self._core.io.write(f'CONFigure:SIGNaling:LTE:CELL:POWer:UL:PUSCh:UE {param}'.rstrip())

	def get(self, cell_name: str) -> float:
		"""SCPI: [CONFigure]:SIGNaling:LTE:CELL:POWer:UL:PUSCh:UE \n
		Snippet: value: float = driver.configure.signaling.lte.cell.power.uplink.pusch.ue.get(cell_name = '1') \n
		Sets the UL power control parameter 'p0-UE-PUSCH'. \n
			:param cell_name: No help available
			:return: p_0_ue_pusch: No help available"""
		param = Conversions.value_to_quoted_str(cell_name)
		response = self._core.io.query_str(f'CONFigure:SIGNaling:LTE:CELL:POWer:UL:PUSCh:UE? {param}')
		return Conversions.str_to_float(response)

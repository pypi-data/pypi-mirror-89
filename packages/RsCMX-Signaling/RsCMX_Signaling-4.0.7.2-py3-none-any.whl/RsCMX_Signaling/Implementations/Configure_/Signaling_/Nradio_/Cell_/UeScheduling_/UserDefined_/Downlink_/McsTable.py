from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.Types import DataType
from .........Internal.ArgSingleList import ArgSingleList
from .........Internal.ArgSingle import ArgSingle
from ......... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class McsTable:
	"""McsTable commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mcsTable", core, parent)

	def set(self, cell_name: str, mcs_table: enums.McsTableB) -> None:
		"""SCPI: [CONFigure]:SIGNaling:NRADio:CELL:UESCheduling:UDEFined:DL:MCSTable \n
		Snippet: driver.configure.signaling.nradio.cell.ueScheduling.userDefined.downlink.mcsTable.set(cell_name = '1', mcs_table = enums.McsTableB.L64) \n
		Selects which MCS table the UE must use to determine the modulation order and the target code rate of the PDSCH, for
		user-defined scheduling. \n
			:param cell_name: No help available
			:param mcs_table: 256-QAM, 64-QAM low SE, 64-QAM
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cell_name', cell_name, DataType.String), ArgSingle('mcs_table', mcs_table, DataType.Enum))
		self._core.io.write(f'CONFigure:SIGNaling:NRADio:CELL:UESCheduling:UDEFined:DL:MCSTable {param}'.rstrip())

	# noinspection PyTypeChecker
	def get(self, cell_name: str) -> enums.McsTableB:
		"""SCPI: [CONFigure]:SIGNaling:NRADio:CELL:UESCheduling:UDEFined:DL:MCSTable \n
		Snippet: value: enums.McsTableB = driver.configure.signaling.nradio.cell.ueScheduling.userDefined.downlink.mcsTable.get(cell_name = '1') \n
		Selects which MCS table the UE must use to determine the modulation order and the target code rate of the PDSCH, for
		user-defined scheduling. \n
			:param cell_name: No help available
			:return: mcs_table: 256-QAM, 64-QAM low SE, 64-QAM"""
		param = Conversions.value_to_quoted_str(cell_name)
		response = self._core.io.query_str(f'CONFigure:SIGNaling:NRADio:CELL:UESCheduling:UDEFined:DL:MCSTable? {param}')
		return Conversions.str_to_scalar_enum(response, enums.McsTableB)

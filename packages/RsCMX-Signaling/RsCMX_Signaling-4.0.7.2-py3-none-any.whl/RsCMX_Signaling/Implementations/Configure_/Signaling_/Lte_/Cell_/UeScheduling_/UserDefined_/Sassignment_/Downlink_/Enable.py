from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from ..........Internal.Types import DataType
from ..........Internal.ArgSingleList import ArgSingleList
from ..........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Enable:
	"""Enable commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("enable", core, parent)

	def set(self, cell_name: str, subframe: float, enable: bool) -> None:
		"""SCPI: [CONFigure]:SIGNaling:LTE:CELL:UESCheduling:UDEFined:SASSignment:DL:ENABle \n
		Snippet: driver.configure.signaling.lte.cell.ueScheduling.userDefined.sassignment.downlink.enable.set(cell_name = '1', subframe = 1.0, enable = False) \n
		Enables or disables scheduling of the DL subframe with the index <Subframe>, for user-defined scheduling. \n
			:param cell_name: No help available
			:param subframe: No help available
			:param enable: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cell_name', cell_name, DataType.String), ArgSingle('subframe', subframe, DataType.Float), ArgSingle('enable', enable, DataType.Boolean))
		self._core.io.write(f'CONFigure:SIGNaling:LTE:CELL:UESCheduling:UDEFined:SASSignment:DL:ENABle {param}'.rstrip())

	def get(self, cell_name: str, subframe: float) -> bool:
		"""SCPI: [CONFigure]:SIGNaling:LTE:CELL:UESCheduling:UDEFined:SASSignment:DL:ENABle \n
		Snippet: value: bool = driver.configure.signaling.lte.cell.ueScheduling.userDefined.sassignment.downlink.enable.get(cell_name = '1', subframe = 1.0) \n
		Enables or disables scheduling of the DL subframe with the index <Subframe>, for user-defined scheduling. \n
			:param cell_name: No help available
			:param subframe: No help available
			:return: enable: No help available"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cell_name', cell_name, DataType.String), ArgSingle('subframe', subframe, DataType.Float))
		response = self._core.io.query_str(f'CONFigure:SIGNaling:LTE:CELL:UESCheduling:UDEFined:SASSignment:DL:ENABle? {param}'.rstrip())
		return Conversions.str_to_bool(response)

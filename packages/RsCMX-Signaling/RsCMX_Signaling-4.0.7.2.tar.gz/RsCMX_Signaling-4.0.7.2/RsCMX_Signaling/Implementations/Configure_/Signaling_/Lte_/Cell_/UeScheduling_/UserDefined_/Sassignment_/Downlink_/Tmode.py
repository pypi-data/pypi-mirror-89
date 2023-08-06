from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from ..........Internal.Types import DataType
from ..........Internal.ArgSingleList import ArgSingleList
from ..........Internal.ArgSingle import ArgSingle
from .......... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tmode:
	"""Tmode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tmode", core, parent)

	def set(self, cell_name: str, tm_ode: enums.TMode) -> None:
		"""SCPI: [CONFigure]:SIGNaling:LTE:CELL:UESCheduling:UDEFined:SASSignment:DL:TMODe \n
		Snippet: driver.configure.signaling.lte.cell.ueScheduling.userDefined.sassignment.downlink.tmode.set(cell_name = '1', tm_ode = enums.TMode.TM1) \n
		Specifies the DL transmission mode, for user-defined scheduling. \n
			:param cell_name: No help available
			:param tm_ode: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cell_name', cell_name, DataType.String), ArgSingle('tm_ode', tm_ode, DataType.Enum))
		self._core.io.write(f'CONFigure:SIGNaling:LTE:CELL:UESCheduling:UDEFined:SASSignment:DL:TMODe {param}'.rstrip())

	# noinspection PyTypeChecker
	def get(self, cell_name: str) -> enums.TMode:
		"""SCPI: [CONFigure]:SIGNaling:LTE:CELL:UESCheduling:UDEFined:SASSignment:DL:TMODe \n
		Snippet: value: enums.TMode = driver.configure.signaling.lte.cell.ueScheduling.userDefined.sassignment.downlink.tmode.get(cell_name = '1') \n
		Specifies the DL transmission mode, for user-defined scheduling. \n
			:param cell_name: No help available
			:return: tm_ode: No help available"""
		param = Conversions.value_to_quoted_str(cell_name)
		response = self._core.io.query_str(f'CONFigure:SIGNaling:LTE:CELL:UESCheduling:UDEFined:SASSignment:DL:TMODe? {param}')
		return Conversions.str_to_scalar_enum(response, enums.TMode)

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Types import DataType
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle
from ........ import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Channel:
	"""Channel commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("channel", core, parent)

	def set(self, cell_name: str, type_py: enums.SrcType) -> None:
		"""SCPI: [CONFigure]:SIGNaling:LTE:CELL:POWer:CONTrol:CHANnel \n
		Snippet: driver.configure.signaling.lte.cell.power.control.channel.set(cell_name = '1', type_py = enums.SrcType.PUCC) \n
		Selects the uplink channel types to which the power control commands are applied. \n
			:param cell_name: No help available
			:param type_py: PUSC: PUSCH PUCC: PUCCH PUPU: PUSCH and PUCCH
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cell_name', cell_name, DataType.String), ArgSingle('type_py', type_py, DataType.Enum))
		self._core.io.write(f'CONFigure:SIGNaling:LTE:CELL:POWer:CONTrol:CHANnel {param}'.rstrip())

	# noinspection PyTypeChecker
	def get(self, cell_name: str) -> enums.SrcType:
		"""SCPI: [CONFigure]:SIGNaling:LTE:CELL:POWer:CONTrol:CHANnel \n
		Snippet: value: enums.SrcType = driver.configure.signaling.lte.cell.power.control.channel.get(cell_name = '1') \n
		Selects the uplink channel types to which the power control commands are applied. \n
			:param cell_name: No help available
			:return: type_py: PUSC: PUSCH PUCC: PUCCH PUPU: PUSCH and PUCCH"""
		param = Conversions.value_to_quoted_str(cell_name)
		response = self._core.io.query_str(f'CONFigure:SIGNaling:LTE:CELL:POWer:CONTrol:CHANnel? {param}')
		return Conversions.str_to_scalar_enum(response, enums.SrcType)

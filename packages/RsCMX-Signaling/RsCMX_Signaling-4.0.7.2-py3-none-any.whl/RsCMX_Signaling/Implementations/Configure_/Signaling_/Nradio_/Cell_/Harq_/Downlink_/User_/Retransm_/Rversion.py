from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from ..........Internal.Types import DataType
from ..........Internal.ArgSingleList import ArgSingleList
from ..........Internal.ArgSingle import ArgSingle
from .......... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rversion:
	"""Rversion commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rversion", core, parent)

	def set(self, cell_name: str, index: int, version: enums.Version) -> None:
		"""SCPI: [CONFigure]:SIGNaling:NRADio:CELL:HARQ:DL:USER:RETRansm:RVERsion \n
		Snippet: driver.configure.signaling.nradio.cell.harq.downlink.user.retransm.rversion.set(cell_name = '1', index = 1, version = enums.Version.AUTO) \n
		Selects a redundancy version for a certain retransmission, for user-defined DL HARQ. \n
			:param cell_name: No help available
			:param index: Index of the retransmission
			:param version: Auto mode, redundancy version number 0 to 3.
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cell_name', cell_name, DataType.String), ArgSingle('index', index, DataType.Integer), ArgSingle('version', version, DataType.Enum))
		self._core.io.write(f'CONFigure:SIGNaling:NRADio:CELL:HARQ:DL:USER:RETRansm:RVERsion {param}'.rstrip())

	# noinspection PyTypeChecker
	def get(self, cell_name: str, index: int) -> enums.Version:
		"""SCPI: [CONFigure]:SIGNaling:NRADio:CELL:HARQ:DL:USER:RETRansm:RVERsion \n
		Snippet: value: enums.Version = driver.configure.signaling.nradio.cell.harq.downlink.user.retransm.rversion.get(cell_name = '1', index = 1) \n
		Selects a redundancy version for a certain retransmission, for user-defined DL HARQ. \n
			:param cell_name: No help available
			:param index: Index of the retransmission
			:return: version: Auto mode, redundancy version number 0 to 3."""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cell_name', cell_name, DataType.String), ArgSingle('index', index, DataType.Integer))
		response = self._core.io.query_str(f'CONFigure:SIGNaling:NRADio:CELL:HARQ:DL:USER:RETRansm:RVERsion? {param}'.rstrip())
		return Conversions.str_to_scalar_enum(response, enums.Version)

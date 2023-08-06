from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from ..........Internal.Types import DataType
from ..........Internal.ArgSingleList import ArgSingleList
from ..........Internal.ArgSingle import ArgSingle
from .......... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Modulation:
	"""Modulation commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("modulation", core, parent)

	def set(self, cell_name: str, index: int, modulation: enums.ModulationB) -> None:
		"""SCPI: [CONFigure]:SIGNaling:NRADio:CELL:HARQ:DL:USER:RETRansm:MODulation \n
		Snippet: driver.configure.signaling.nradio.cell.harq.downlink.user.retransm.modulation.set(cell_name = '1', index = 1, modulation = enums.ModulationB.AUTO) \n
		Selects a modulation scheme for a certain retransmission, for user-defined DL HARQ. \n
			:param cell_name: No help available
			:param index: Index of the retransmission
			:param modulation: BPSK, auto mode, π/2-BPSK, QPSK, 16-QAM, 64-QAM, 256-QAM
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cell_name', cell_name, DataType.String), ArgSingle('index', index, DataType.Integer), ArgSingle('modulation', modulation, DataType.Enum))
		self._core.io.write(f'CONFigure:SIGNaling:NRADio:CELL:HARQ:DL:USER:RETRansm:MODulation {param}'.rstrip())

	# noinspection PyTypeChecker
	def get(self, cell_name: str, index: int) -> enums.ModulationB:
		"""SCPI: [CONFigure]:SIGNaling:NRADio:CELL:HARQ:DL:USER:RETRansm:MODulation \n
		Snippet: value: enums.ModulationB = driver.configure.signaling.nradio.cell.harq.downlink.user.retransm.modulation.get(cell_name = '1', index = 1) \n
		Selects a modulation scheme for a certain retransmission, for user-defined DL HARQ. \n
			:param cell_name: No help available
			:param index: Index of the retransmission
			:return: modulation: BPSK, auto mode, π/2-BPSK, QPSK, 16-QAM, 64-QAM, 256-QAM"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cell_name', cell_name, DataType.String), ArgSingle('index', index, DataType.Integer))
		response = self._core.io.query_str(f'CONFigure:SIGNaling:NRADio:CELL:HARQ:DL:USER:RETRansm:MODulation? {param}'.rstrip())
		return Conversions.str_to_scalar_enum(response, enums.ModulationB)

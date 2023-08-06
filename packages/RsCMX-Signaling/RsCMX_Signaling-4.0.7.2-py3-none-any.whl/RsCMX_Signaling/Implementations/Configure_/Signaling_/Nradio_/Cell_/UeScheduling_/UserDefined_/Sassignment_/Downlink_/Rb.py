from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal.Types import DataType
from ..........Internal.StructBase import StructBase
from ..........Internal.ArgStruct import ArgStruct
from ..........Internal.ArgSingleList import ArgSingleList
from ..........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rb:
	"""Rb commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rb", core, parent)

	def set(self, cell_name: str, slot: float, number_rb: int, start_rb: int) -> None:
		"""SCPI: [CONFigure]:SIGNaling:NRADio:CELL:UESCheduling:UDEFined:SASSignment:DL:RB \n
		Snippet: driver.configure.signaling.nradio.cell.ueScheduling.userDefined.sassignment.downlink.rb.set(cell_name = '1', slot = 1.0, number_rb = 1, start_rb = 1) \n
		Specifies the scheduled RB allocation for the DL slot with the index <Slot>, for user-defined scheduling. \n
			:param cell_name: No help available
			:param slot: No help available
			:param number_rb: No help available
			:param start_rb: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cell_name', cell_name, DataType.String), ArgSingle('slot', slot, DataType.Float), ArgSingle('number_rb', number_rb, DataType.Integer), ArgSingle('start_rb', start_rb, DataType.Integer))
		self._core.io.write(f'CONFigure:SIGNaling:NRADio:CELL:UESCheduling:UDEFined:SASSignment:DL:RB {param}'.rstrip())

	# noinspection PyTypeChecker
	class GetStruct(StructBase):
		"""Response structure. Fields: \n
			- Number_Rb: int: No parameter help available
			- Start_Rb: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Number_Rb'),
			ArgStruct.scalar_int('Start_Rb')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Number_Rb: int = None
			self.Start_Rb: int = None

	def get(self, cell_name: str, slot: float) -> GetStruct:
		"""SCPI: [CONFigure]:SIGNaling:NRADio:CELL:UESCheduling:UDEFined:SASSignment:DL:RB \n
		Snippet: value: GetStruct = driver.configure.signaling.nradio.cell.ueScheduling.userDefined.sassignment.downlink.rb.get(cell_name = '1', slot = 1.0) \n
		Specifies the scheduled RB allocation for the DL slot with the index <Slot>, for user-defined scheduling. \n
			:param cell_name: No help available
			:param slot: No help available
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cell_name', cell_name, DataType.String), ArgSingle('slot', slot, DataType.Float))
		return self._core.io.query_struct(f'CONFigure:SIGNaling:NRADio:CELL:UESCheduling:UDEFined:SASSignment:DL:RB? {param}'.rstrip(), self.__class__.GetStruct())

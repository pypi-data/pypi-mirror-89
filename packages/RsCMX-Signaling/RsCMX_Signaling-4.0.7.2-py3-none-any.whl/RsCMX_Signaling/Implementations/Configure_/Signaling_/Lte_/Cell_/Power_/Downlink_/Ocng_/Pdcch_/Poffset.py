from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from ..........Internal.Types import DataType
from ..........Internal.StructBase import StructBase
from ..........Internal.ArgStruct import ArgStruct
from ..........Internal.ArgSingleList import ArgSingleList
from ..........Internal.ArgSingle import ArgSingle
from .......... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Poffset:
	"""Poffset commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("poffset", core, parent)

	def set(self, cell_name: str, mode: enums.Mode, value: float = None) -> None:
		"""SCPI: [CONFigure]:SIGNaling:LTE:CELL:POWer:DL:OCNG:PDCCh:POFFset \n
		Snippet: driver.configure.signaling.lte.cell.power.downlink.ocng.pdcch.poffset.set(cell_name = '1', mode = enums.Mode.MAX, value = 1.0) \n
		Defines the power level of the PDCCH for OCNG. \n
			:param cell_name: No help available
			:param mode: No help available
			:param value: Power level relative to the RS EPRE, for Mode = UDEFined.
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cell_name', cell_name, DataType.String), ArgSingle('mode', mode, DataType.Enum), ArgSingle('value', value, DataType.Float, True))
		self._core.io.write(f'CONFigure:SIGNaling:LTE:CELL:POWer:DL:OCNG:PDCCh:POFFset {param}'.rstrip())

	# noinspection PyTypeChecker
	class GetStruct(StructBase):
		"""Response structure. Fields: \n
			- Mode: enums.Mode: No parameter help available
			- Value: float: Power level relative to the RS EPRE, for Mode = UDEFined."""
		__meta_args_list = [
			ArgStruct.scalar_enum('Mode', enums.Mode),
			ArgStruct.scalar_float('Value')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Mode: enums.Mode = None
			self.Value: float = None

	def get(self, cell_name: str) -> GetStruct:
		"""SCPI: [CONFigure]:SIGNaling:LTE:CELL:POWer:DL:OCNG:PDCCh:POFFset \n
		Snippet: value: GetStruct = driver.configure.signaling.lte.cell.power.downlink.ocng.pdcch.poffset.get(cell_name = '1') \n
		Defines the power level of the PDCCH for OCNG. \n
			:param cell_name: No help available
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		param = Conversions.value_to_quoted_str(cell_name)
		return self._core.io.query_struct(f'CONFigure:SIGNaling:LTE:CELL:POWer:DL:OCNG:PDCCh:POFFset? {param}', self.__class__.GetStruct())

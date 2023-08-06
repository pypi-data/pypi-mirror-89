from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Mm_5_Greg_State_Sum: enums.RegState: No parameter help available
			- Mm_5_Greg_State: enums.RegState: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Mm_5_Greg_State_Sum', enums.RegState),
			ArgStruct.scalar_enum('Mm_5_Greg_State', enums.RegState)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Mm_5_Greg_State_Sum: enums.RegState = None
			self.Mm_5_Greg_State: enums.RegState = None

	def fetch(self, ue_id: str = None) -> FetchStruct:
		"""SCPI: FETCh:SIGNaling:TOPology:FGS:UE:STATe \n
		Snippet: value: FetchStruct = driver.signaling.topology.fgs.ue.state.fetch(ue_id = '1') \n
		Queries the UE registration state for 5G tracking areas. \n
			:param ue_id: No help available
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		param = ArgSingleList().compose_cmd_string(ArgSingle('ue_id', ue_id, DataType.String, True))
		return self._core.io.query_struct(f'FETCh:SIGNaling:TOPology:FGS:UE:STATe? {param}'.rstrip(), self.__class__.FetchStruct())

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Types import DataType
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle
from ........ import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IptPower:
	"""IptPower commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("iptPower", core, parent)

	def set(self, cell_name: str, power: enums.Power) -> None:
		"""SCPI: [CONFigure]:SIGNaling:LTE:CELL:POWer:UL:IPTPower \n
		Snippet: driver.configure.signaling.lte.cell.power.uplink.iptPower.set(cell_name = '1', power = enums.Power.P100) \n
		Sets the parameter 'preambleInitialReceivedTargetPower', signaled to the UE as common RACH parameter. \n
			:param cell_name: No help available
			:param power: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cell_name', cell_name, DataType.String), ArgSingle('power', power, DataType.Enum))
		self._core.io.write(f'CONFigure:SIGNaling:LTE:CELL:POWer:UL:IPTPower {param}'.rstrip())

	# noinspection PyTypeChecker
	def get(self, cell_name: str) -> enums.Power:
		"""SCPI: [CONFigure]:SIGNaling:LTE:CELL:POWer:UL:IPTPower \n
		Snippet: value: enums.Power = driver.configure.signaling.lte.cell.power.uplink.iptPower.get(cell_name = '1') \n
		Sets the parameter 'preambleInitialReceivedTargetPower', signaled to the UE as common RACH parameter. \n
			:param cell_name: No help available
			:return: power: No help available"""
		param = Conversions.value_to_quoted_str(cell_name)
		response = self._core.io.query_str(f'CONFigure:SIGNaling:LTE:CELL:POWer:UL:IPTPower? {param}')
		return Conversions.str_to_scalar_enum(response, enums.Power)

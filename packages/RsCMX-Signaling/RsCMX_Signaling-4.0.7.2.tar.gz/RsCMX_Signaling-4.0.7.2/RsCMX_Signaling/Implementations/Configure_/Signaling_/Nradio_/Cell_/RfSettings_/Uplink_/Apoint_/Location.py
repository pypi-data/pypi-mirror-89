from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.Types import DataType
from .........Internal.ArgSingleList import ArgSingleList
from .........Internal.ArgSingle import ArgSingle
from ......... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Location:
	"""Location commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("location", core, parent)

	def set(self, cell_name: str, location: enums.Location) -> None:
		"""SCPI: [CONFigure]:SIGNaling:NRADio:CELL:RFSettings:UL:APOint:LOCation \n
		Snippet: driver.configure.signaling.nradio.cell.rfSettings.uplink.apoint.location.set(cell_name = '1', location = enums.Location.HIGH) \n
		Selects a method for defining the frequency of point A, for the uplink. \n
			:param cell_name: No help available
			:param location:
				- MID, LOW, HIGH: Automatic selection of mid, low or high position in the frequency band.
				- USER: User-defined frequency, specified via separate command."""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cell_name', cell_name, DataType.String), ArgSingle('location', location, DataType.Enum))
		self._core.io.write(f'CONFigure:SIGNaling:NRADio:CELL:RFSettings:UL:APOint:LOCation {param}'.rstrip())

	# noinspection PyTypeChecker
	def get(self, cell_name: str) -> enums.Location:
		"""SCPI: [CONFigure]:SIGNaling:NRADio:CELL:RFSettings:UL:APOint:LOCation \n
		Snippet: value: enums.Location = driver.configure.signaling.nradio.cell.rfSettings.uplink.apoint.location.get(cell_name = '1') \n
		Selects a method for defining the frequency of point A, for the uplink. \n
			:param cell_name: No help available
			:return: location:
				- MID, LOW, HIGH: Automatic selection of mid, low or high position in the frequency band.
				- USER: User-defined frequency, specified via separate command."""
		param = Conversions.value_to_quoted_str(cell_name)
		response = self._core.io.query_str(f'CONFigure:SIGNaling:NRADio:CELL:RFSettings:UL:APOint:LOCation? {param}')
		return Conversions.str_to_scalar_enum(response, enums.Location)

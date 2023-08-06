from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Plmn:
	"""Plmn commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("plmn", core, parent)

	def set(self, name_plmn: str, mcc: str = None, mnc: str = None) -> None:
		"""SCPI: CREate:SIGNaling:TOPology:PLMN \n
		Snippet: driver.create.signaling.topology.plmn.set(name_plmn = '1', mcc = '1', mnc = '1') \n
		Creates a PLMN and optionally defines MCC and MNC of the PLMN. \n
			:param name_plmn: Assigns a name to the PLMN. The string is used in other commands to select this PLMN.
			:param mcc: No help available
			:param mnc: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('name_plmn', name_plmn, DataType.String), ArgSingle('mcc', mcc, DataType.String, True), ArgSingle('mnc', mnc, DataType.String, True))
		self._core.io.write(f'CREate:SIGNaling:TOPology:PLMN {param}'.rstrip())

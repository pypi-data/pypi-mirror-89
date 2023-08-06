from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pattern:
	"""Pattern commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pattern", core, parent)

	def set_execute(self, cell_name: str) -> None:
		"""SCPI: PROCedure:SIGNaling:LTE:CELL:POWer:CONTrol:TPControl:PATTern:EXECute \n
		Snippet: driver.procedure.signaling.lte.cell.power.control.tpControl.pattern.set_execute(cell_name = '1') \n
		Starts the execution of a user-defined TPC pattern. \n
			:param cell_name: No help available
		"""
		param = Conversions.value_to_quoted_str(cell_name)
		self._core.io.write(f'PROCedure:SIGNaling:LTE:CELL:POWer:CONTrol:TPControl:PATTern:EXECute {param}')

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.StructBase import StructBase
from ...Internal.ArgStruct import ArgStruct
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Signaling:
	"""Signaling commands group definition. 5 total commands, 3 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("signaling", core, parent)

	@property
	def ue(self):
		"""ue commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ue'):
			from .Signaling_.Ue import Ue
			self._ue = Ue(self._core, self._base)
		return self._ue

	@property
	def lte(self):
		"""lte commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_lte'):
			from .Signaling_.Lte import Lte
			self._lte = Lte(self._core, self._base)
		return self._lte

	@property
	def nradio(self):
		"""nradio commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_nradio'):
			from .Signaling_.Nradio import Nradio
			self._nradio = Nradio(self._core, self._base)
		return self._nradio

	# noinspection PyTypeChecker
	class SmsStruct(StructBase):
		"""Structure for setting input parameters. Contains optional set arguments. Fields: \n
			- Address: str: Address of the originator of the message
			- Message: str: Message text
			- Type_Py: enums.Type: Optional setting parameter. Coding group GDC: general data coding DCMC: data coding / message class
			- Coding: enums.Coding: Optional setting parameter. Data coding, selecting the used character set GSM: GSM 7-bit default alphabet coding (ASCII) EIGHt: 8-bit binary data UCS2: UCS-2 16-bit coding (only for GDC, not for DCMC)
			- Class: enums.Class: Optional setting parameter. Message class 0 to 3, selecting to which component of the UE the message is delivered.
			- Core_Network: enums.CoreNetwork: Optional setting parameter. Type of network delivering the message, EPS or 5G"""
		__meta_args_list = [
			ArgStruct.scalar_str('Address'),
			ArgStruct.scalar_str('Message'),
			ArgStruct.scalar_enum_optional('Type_Py', enums.Type),
			ArgStruct.scalar_enum_optional('Coding', enums.Coding),
			ArgStruct.scalar_enum_optional('Class', enums.Class),
			ArgStruct.scalar_enum_optional('Core_Network', enums.CoreNetwork)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Address: str = None
			self.Message: str = None
			self.Type_Py: enums.Type = None
			self.Coding: enums.Coding = None
			self.Class: enums.Class = None
			self.Core_Network: enums.CoreNetwork = None

	def set_sms(self, value: SmsStruct) -> None:
		"""SCPI: PROCedure:SIGNaling:SMS \n
		Snippet: driver.procedure.signaling.set_sms(value = SmsStruct()) \n
		Sends a short message to the UE. For background information, see 3GPP TS 23.038. \n
			:param value: see the help for SmsStruct structure arguments.
		"""
		self._core.io.write_struct('PROCedure:SIGNaling:SMS', value)

	def clone(self) -> 'Signaling':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Signaling(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

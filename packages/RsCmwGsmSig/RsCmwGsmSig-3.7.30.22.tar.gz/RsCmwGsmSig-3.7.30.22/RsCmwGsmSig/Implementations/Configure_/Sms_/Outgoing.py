from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Outgoing:
	"""Outgoing commands group definition. 13 total commands, 1 Sub-groups, 10 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("outgoing", core, parent)

	@property
	def sctStamp(self):
		"""sctStamp commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_sctStamp'):
			from .Outgoing_.SctStamp import SctStamp
			self._sctStamp = SctStamp(self._core, self._base)
		return self._sctStamp

	# noinspection PyTypeChecker
	def get_sdomain(self) -> enums.SmsDomain:
		"""SCPI: CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:SDOMain \n
		Snippet: value: enums.SmsDomain = driver.configure.sms.outgoing.get_sdomain() \n
		Selects the core network domain for the outgoing SMS. \n
			:return: smsdomain: AUTO | CS | PS AUTO: domain of actual connection CS: circuit switched domain PS: packet switched domain
		"""
		response = self._core.io.query_str('CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:SDOMain?')
		return Conversions.str_to_scalar_enum(response, enums.SmsDomain)

	def set_sdomain(self, smsdomain: enums.SmsDomain) -> None:
		"""SCPI: CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:SDOMain \n
		Snippet: driver.configure.sms.outgoing.set_sdomain(smsdomain = enums.SmsDomain.AUTO) \n
		Selects the core network domain for the outgoing SMS. \n
			:param smsdomain: AUTO | CS | PS AUTO: domain of actual connection CS: circuit switched domain PS: packet switched domain
		"""
		param = Conversions.enum_scalar_to_str(smsdomain, enums.SmsDomain)
		self._core.io.write(f'CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:SDOMain {param}')

	def get_internal(self) -> str:
		"""SCPI: CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:INTernal \n
		Snippet: value: str = driver.configure.sms.outgoing.get_internal() \n
		Defines the message text for SMS messages to be sent to the MS. It is encoded as 7-bit ASCII text. \n
			:return: sms_internal: String with up to 800 characters
		"""
		response = self._core.io.query_str('CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:INTernal?')
		return trim_str_response(response)

	def set_internal(self, sms_internal: str) -> None:
		"""SCPI: CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:INTernal \n
		Snippet: driver.configure.sms.outgoing.set_internal(sms_internal = '1') \n
		Defines the message text for SMS messages to be sent to the MS. It is encoded as 7-bit ASCII text. \n
			:param sms_internal: String with up to 800 characters
		"""
		param = Conversions.value_to_quoted_str(sms_internal)
		self._core.io.write(f'CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:INTernal {param}')

	def get_binary(self) -> float:
		"""SCPI: CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:BINary \n
		Snippet: value: float = driver.configure.sms.outgoing.get_binary() \n
		Defines the SMS message encoded as 8-bit binary data. \n
			:return: smsbinary: SMS message in hexadecimal format.
		"""
		response = self._core.io.query_str('CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:BINary?')
		return Conversions.str_to_float(response)

	def set_binary(self, smsbinary: float) -> None:
		"""SCPI: CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:BINary \n
		Snippet: driver.configure.sms.outgoing.set_binary(smsbinary = 1.0) \n
		Defines the SMS message encoded as 8-bit binary data. \n
			:param smsbinary: SMS message in hexadecimal format.
		"""
		param = Conversions.decimal_value_to_str(smsbinary)
		self._core.io.write(f'CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:BINary {param}')

	# noinspection PyTypeChecker
	def get_dcoding(self) -> enums.SmsDataCoding:
		"""SCPI: CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:DCODing \n
		Snippet: value: enums.SmsDataCoding = driver.configure.sms.outgoing.get_dcoding() \n
		Defines the short message coding. \n
			:return: data_coding: BIT7 | BIT8 BIT7: GSM 7-bit default alphabet BIT8: 8-bit data for SMS binary
		"""
		response = self._core.io.query_str('CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:DCODing?')
		return Conversions.str_to_scalar_enum(response, enums.SmsDataCoding)

	def set_dcoding(self, data_coding: enums.SmsDataCoding) -> None:
		"""SCPI: CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:DCODing \n
		Snippet: driver.configure.sms.outgoing.set_dcoding(data_coding = enums.SmsDataCoding.BIT7) \n
		Defines the short message coding. \n
			:param data_coding: BIT7 | BIT8 BIT7: GSM 7-bit default alphabet BIT8: 8-bit data for SMS binary
		"""
		param = Conversions.enum_scalar_to_str(data_coding, enums.SmsDataCoding)
		self._core.io.write(f'CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:DCODing {param}')

	# noinspection PyTypeChecker
	def get_cgroup(self) -> enums.CodingGroup:
		"""SCPI: CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:CGRoup \n
		Snippet: value: enums.CodingGroup = driver.configure.sms.outgoing.get_cgroup() \n
		Defines how to interpret SMS signaling information. Coding groups are defined in 3GPP TS 23.038 chapter 4. \n
			:return: coding_group: GDCoding | DCMClass GDCoding: general data coding DCMClass: data coding / message class
		"""
		response = self._core.io.query_str('CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:CGRoup?')
		return Conversions.str_to_scalar_enum(response, enums.CodingGroup)

	def set_cgroup(self, coding_group: enums.CodingGroup) -> None:
		"""SCPI: CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:CGRoup \n
		Snippet: driver.configure.sms.outgoing.set_cgroup(coding_group = enums.CodingGroup.DCMClass) \n
		Defines how to interpret SMS signaling information. Coding groups are defined in 3GPP TS 23.038 chapter 4. \n
			:param coding_group: GDCoding | DCMClass GDCoding: general data coding DCMClass: data coding / message class
		"""
		param = Conversions.enum_scalar_to_str(coding_group, enums.CodingGroup)
		self._core.io.write(f'CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:CGRoup {param}')

	# noinspection PyTypeChecker
	def get_mclass(self) -> enums.MessageClass:
		"""SCPI: CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:MCLass \n
		Snippet: value: enums.MessageClass = driver.configure.sms.outgoing.get_mclass() \n
		Specifies default routing of SMS as defined in 3GPP TS 23.038. The MS settings override any default meaning by selecting
		its own routing. \n
			:return: message_class: CL0 | CL1 | CL2 | CL3 | NONE CL0: class 0, SMS not to be stored automatically CL1: SMS to be stored in mobile equipment CL2: SMS to be stored in SIM CL3: SMS to be stored in terminal equipment (see 3GPP TS 07.05) NONE: no message class (relevant only for general data coding)
		"""
		response = self._core.io.query_str('CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:MCLass?')
		return Conversions.str_to_scalar_enum(response, enums.MessageClass)

	def set_mclass(self, message_class: enums.MessageClass) -> None:
		"""SCPI: CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:MCLass \n
		Snippet: driver.configure.sms.outgoing.set_mclass(message_class = enums.MessageClass.CL0) \n
		Specifies default routing of SMS as defined in 3GPP TS 23.038. The MS settings override any default meaning by selecting
		its own routing. \n
			:param message_class: CL0 | CL1 | CL2 | CL3 | NONE CL0: class 0, SMS not to be stored automatically CL1: SMS to be stored in mobile equipment CL2: SMS to be stored in SIM CL3: SMS to be stored in terminal equipment (see 3GPP TS 07.05) NONE: no message class (relevant only for general data coding)
		"""
		param = Conversions.enum_scalar_to_str(message_class, enums.MessageClass)
		self._core.io.write(f'CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:MCLass {param}')

	def get_os_address(self) -> str:
		"""SCPI: CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:OSADdress \n
		Snippet: value: str = driver.configure.sms.outgoing.get_os_address() \n
		Specifies the phone number of SMS center. \n
			:return: orig_orig_smsc_address: No help available
		"""
		response = self._core.io.query_str('CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:OSADdress?')
		return trim_str_response(response)

	def set_os_address(self, orig_orig_smsc_address: str) -> None:
		"""SCPI: CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:OSADdress \n
		Snippet: driver.configure.sms.outgoing.set_os_address(orig_orig_smsc_address = '1') \n
		Specifies the phone number of SMS center. \n
			:param orig_orig_smsc_address: No help available
		"""
		param = Conversions.value_to_quoted_str(orig_orig_smsc_address)
		self._core.io.write(f'CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:OSADdress {param}')

	def get_oaddress(self) -> str:
		"""SCPI: CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:OADDress \n
		Snippet: value: str = driver.configure.sms.outgoing.get_oaddress() \n
		Specifies the phone number of the device which has sent SMS. \n
			:return: orig_address: No help available
		"""
		response = self._core.io.query_str('CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:OADDress?')
		return trim_str_response(response)

	def set_oaddress(self, orig_address: str) -> None:
		"""SCPI: CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:OADDress \n
		Snippet: driver.configure.sms.outgoing.set_oaddress(orig_address = '1') \n
		Specifies the phone number of the device which has sent SMS. \n
			:param orig_address: No help available
		"""
		param = Conversions.value_to_quoted_str(orig_address)
		self._core.io.write(f'CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:OADDress {param}')

	def get_udheader(self) -> float or bool:
		"""SCPI: CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:UDHeader \n
		Snippet: value: float or bool = driver.configure.sms.outgoing.get_udheader() \n
		Configures the TP user data header. \n
			:return: header: Up to 16 hexadecimal digits Range: #H0 to #HFFFFFFFFFFFFFFFF Additional parameters: OFF | ON (disables | enables sending the header)
		"""
		response = self._core.io.query_str('CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:UDHeader?')
		return Conversions.str_to_float_or_bool(response)

	def set_udheader(self, header: float or bool) -> None:
		"""SCPI: CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:UDHeader \n
		Snippet: driver.configure.sms.outgoing.set_udheader(header = 1.0) \n
		Configures the TP user data header. \n
			:param header: Up to 16 hexadecimal digits Range: #H0 to #HFFFFFFFFFFFFFFFF Additional parameters: OFF | ON (disables | enables sending the header)
		"""
		param = Conversions.decimal_or_bool_value_to_str(header)
		self._core.io.write(f'CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:UDHeader {param}')

	def get_pidentifier(self) -> float:
		"""SCPI: CONFigure:GSM:SIGNaling<instance>:SMS:OUTGoing:PIDentifier \n
		Snippet: value: float = driver.configure.sms.outgoing.get_pidentifier() \n
		Specifies the TP protocol identifier (TP-PID) value to be sent. \n
			:return: idn: Range: #H0 to #HFF
		"""
		response = self._core.io.query_str('CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:PIDentifier?')
		return Conversions.str_to_float(response)

	def set_pidentifier(self, idn: float) -> None:
		"""SCPI: CONFigure:GSM:SIGNaling<instance>:SMS:OUTGoing:PIDentifier \n
		Snippet: driver.configure.sms.outgoing.set_pidentifier(idn = 1.0) \n
		Specifies the TP protocol identifier (TP-PID) value to be sent. \n
			:param idn: Range: #H0 to #HFF
		"""
		param = Conversions.decimal_value_to_str(idn)
		self._core.io.write(f'CONFigure:GSM:SIGNaling<Instance>:SMS:OUTGoing:PIDentifier {param}')

	def clone(self) -> 'Outgoing':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Outgoing(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

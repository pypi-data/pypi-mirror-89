from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Carrier:
	"""Carrier commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: Carrier, default value after init: Carrier.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("carrier", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_carrier_get', 'repcap_carrier_set', repcap.Carrier.Nr1)

	def repcap_carrier_set(self, enum_value: repcap.Carrier) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Carrier.Default
		Default value after init: Carrier.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_carrier_get(self) -> repcap.Carrier:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def set(self, coding_scheme: List[enums.DownlinkCodingScheme], carrier=repcap.Carrier.Default) -> None:
		"""SCPI: PREPare:GSM:SIGNaling<Instance>:HANDover:PSWitched:CSCHeme:DL:CARRier<Carrier> \n
		Snippet: driver.prepare.handover.pswitched.cscheme.downlink.carrier.set(coding_scheme = [DownlinkCodingScheme.C1, DownlinkCodingScheme.ON], carrier = repcap.Carrier.Default) \n
		Selects the coding schemes for all downlink timeslots in the destination GSM band (packet switched domain) . The selected
		values must be compatible to the configured TBF level, see method RsCmwGsmSig.Configure.Connection.Pswitched.tlevel.
		In the current software version, the same value applies to all downlink slots and to both carriers. You cannot set
		different values. \n
			:param coding_scheme: C1 | C2 | C3 | C4 | MC1 | MC2 | MC3 | MC4 | MC5 | MC6 | MC7 | MC8 | MC9 | DA5 | DA6 | DA7 | DA8 | DA9 | DA10 | DA11 | DA12 | ON | OFF List of 8 coding schemes for slot 0 to 7. All 8 values must be identical. C1 to C4: CS-1 to CS-4 MC1 to MC9: MCS-1 to MCS-9 DA5 to DA12: DAS-5 to DAS-12 OFF (ON) disables (enables) the coding scheme
			:param carrier: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Carrier')"""
		param = Conversions.enum_list_to_str(coding_scheme, enums.DownlinkCodingScheme)
		carrier_cmd_val = self._base.get_repcap_cmd_value(carrier, repcap.Carrier)
		self._core.io.write_with_opc(f'PREPare:GSM:SIGNaling<Instance>:HANDover:PSWitched:CSCHeme:DL:CARRier{carrier_cmd_val} {param}')

	# noinspection PyTypeChecker
	def get(self, carrier=repcap.Carrier.Default) -> List[enums.DownlinkCodingScheme]:
		"""SCPI: PREPare:GSM:SIGNaling<Instance>:HANDover:PSWitched:CSCHeme:DL:CARRier<Carrier> \n
		Snippet: value: List[enums.DownlinkCodingScheme] = driver.prepare.handover.pswitched.cscheme.downlink.carrier.get(carrier = repcap.Carrier.Default) \n
		Selects the coding schemes for all downlink timeslots in the destination GSM band (packet switched domain) . The selected
		values must be compatible to the configured TBF level, see method RsCmwGsmSig.Configure.Connection.Pswitched.tlevel.
		In the current software version, the same value applies to all downlink slots and to both carriers. You cannot set
		different values. \n
			:param carrier: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Carrier')
			:return: coding_scheme: C1 | C2 | C3 | C4 | MC1 | MC2 | MC3 | MC4 | MC5 | MC6 | MC7 | MC8 | MC9 | DA5 | DA6 | DA7 | DA8 | DA9 | DA10 | DA11 | DA12 | ON | OFF List of 8 coding schemes for slot 0 to 7. All 8 values must be identical. C1 to C4: CS-1 to CS-4 MC1 to MC9: MCS-1 to MCS-9 DA5 to DA12: DAS-5 to DAS-12 OFF (ON) disables (enables) the coding scheme"""
		carrier_cmd_val = self._base.get_repcap_cmd_value(carrier, repcap.Carrier)
		response = self._core.io.query_str_with_opc(f'PREPare:GSM:SIGNaling<Instance>:HANDover:PSWitched:CSCHeme:DL:CARRier{carrier_cmd_val}?')
		return Conversions.str_to_list_enum(response, enums.DownlinkCodingScheme)

	def clone(self) -> 'Carrier':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Carrier(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

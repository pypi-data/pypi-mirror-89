from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CpSymbols:
	"""CpSymbols commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cpSymbols", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def repcap_channel_set(self, enum_value: repcap.Channel) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Channel.Default
		Default value after init: Channel.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_channel_get(self) -> repcap.Channel:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def set(self, cp_symbols: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:OFDM:CPSYmbols<CH> \n
		Snippet: driver.source.bb.ofdm.cpSymbols.set(cp_symbols = 1, channel = repcap.Channel.Default) \n
		For f-OFDM/OFDM, defines number of symbols on that the cyclic prefix/the alternative cyclic prefix is applied. \n
			:param cp_symbols: integer Range: 0 to 8192
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'CpSymbols')"""
		param = Conversions.decimal_value_to_str(cp_symbols)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:OFDM:CPSYmbols{channel_cmd_val} {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:OFDM:CPSYmbols<CH> \n
		Snippet: value: int = driver.source.bb.ofdm.cpSymbols.get(channel = repcap.Channel.Default) \n
		For f-OFDM/OFDM, defines number of symbols on that the cyclic prefix/the alternative cyclic prefix is applied. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'CpSymbols')
			:return: cp_symbols: integer Range: 0 to 8192"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:OFDM:CPSYmbols{channel_cmd_val}?')
		return Conversions.str_to_int(response)

	def clone(self) -> 'CpSymbols':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CpSymbols(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

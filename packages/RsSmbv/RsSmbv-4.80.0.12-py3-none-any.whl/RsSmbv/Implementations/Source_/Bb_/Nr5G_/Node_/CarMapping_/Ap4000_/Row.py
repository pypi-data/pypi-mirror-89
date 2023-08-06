from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Row:
	"""Row commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("row", core, parent)
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

	def set(self, ap_4000: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CARMapping:AP4000:[ROW<CH>] \n
		Snippet: driver.source.bb.nr5G.node.carMapping.ap4000.row.set(ap_4000 = False, channel = repcap.Channel.Default) \n
		Sets if the SS/PBCHs are output at the selected output. \n
			:param ap_4000: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Row')"""
		param = Conversions.bool_to_str(ap_4000)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CARMapping:AP4000:ROW{channel_cmd_val} {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CARMapping:AP4000:[ROW<CH>] \n
		Snippet: value: bool = driver.source.bb.nr5G.node.carMapping.ap4000.row.get(channel = repcap.Channel.Default) \n
		Sets if the SS/PBCHs are output at the selected output. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Row')
			:return: ap_4000: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CARMapping:AP4000:ROW{channel_cmd_val}?')
		return Conversions.str_to_bool(response)

	def clone(self) -> 'Row':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Row(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

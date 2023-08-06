from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ValSubFrames:
	"""ValSubFrames commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("valSubFrames", core, parent)
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

	def set(self, valid_sub_frames: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:EMTC:BMP:VALSubframes<CH> \n
		Snippet: driver.source.bb.eutra.dl.emtc.bmp.valSubFrames.set(valid_sub_frames = False, channel = repcap.Channel.Default) \n
		No command help available \n
			:param valid_sub_frames: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'ValSubFrames')"""
		param = Conversions.bool_to_str(valid_sub_frames)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:BMP:VALSubframes{channel_cmd_val} {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:EMTC:BMP:VALSubframes<CH> \n
		Snippet: value: bool = driver.source.bb.eutra.dl.emtc.bmp.valSubFrames.get(channel = repcap.Channel.Default) \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'ValSubFrames')
			:return: valid_sub_frames: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:BMP:VALSubframes{channel_cmd_val}?')
		return Conversions.str_to_bool(response)

	def clone(self) -> 'ValSubFrames':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ValSubFrames(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

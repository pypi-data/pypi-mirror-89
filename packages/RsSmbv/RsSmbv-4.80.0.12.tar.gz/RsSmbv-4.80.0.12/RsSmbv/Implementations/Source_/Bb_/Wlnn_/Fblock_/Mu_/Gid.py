from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Gid:
	"""Gid commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("gid", core, parent)

	def set(self, gid: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:MU<ST>:GID \n
		Snippet: driver.source.bb.wlnn.fblock.mu.gid.set(gid = 1, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the group ID for all available users. \n
			:param gid: integer Range: 1 to 62
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mu')"""
		param = Conversions.decimal_value_to_str(gid)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:MU{stream_cmd_val}:GID {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:MU<ST>:GID \n
		Snippet: value: int = driver.source.bb.wlnn.fblock.mu.gid.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the group ID for all available users. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mu')
			:return: gid: integer Range: 1 to 62"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:MU{stream_cmd_val}:GID?')
		return Conversions.str_to_int(response)

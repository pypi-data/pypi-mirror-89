from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, state: bool, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GPS<ST>:SIGNal:L2Band:C1C:[STATe] \n
		Snippet: driver.source.bb.gnss.svid.gps.signal.l2Band.c1C.state.set(state = False, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		No command help available \n
			:param state: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')"""
		param = Conversions.bool_to_str(state)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GPS{stream_cmd_val}:SIGNal:L2Band:C1C:STATe {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GPS<ST>:SIGNal:L2Band:C1C:[STATe] \n
		Snippet: value: bool = driver.source.bb.gnss.svid.gps.signal.l2Band.c1C.state.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')
			:return: state: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GPS{stream_cmd_val}:SIGNal:L2Band:C1C:STATe?')
		return Conversions.str_to_bool(response)

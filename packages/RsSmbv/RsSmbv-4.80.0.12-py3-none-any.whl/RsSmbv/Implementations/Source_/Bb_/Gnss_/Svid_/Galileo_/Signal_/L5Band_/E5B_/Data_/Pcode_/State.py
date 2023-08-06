from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, state: bool, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GALileo<ST>:SIGNal:L5Band:E5B:DATA:PCODe:[STATe] \n
		Snippet: driver.source.bb.gnss.svid.galileo.signal.l5Band.e5B.data.pcode.state.set(state = False, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Activates spreading by using the primary code. \n
			:param state: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Galileo')"""
		param = Conversions.bool_to_str(state)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GALileo{stream_cmd_val}:SIGNal:L5Band:E5B:DATA:PCODe:STATe {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GALileo<ST>:SIGNal:L5Band:E5B:DATA:PCODe:[STATe] \n
		Snippet: value: bool = driver.source.bb.gnss.svid.galileo.signal.l5Band.e5B.data.pcode.state.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Activates spreading by using the primary code. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Galileo')
			:return: state: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GALileo{stream_cmd_val}:SIGNal:L5Band:E5B:DATA:PCODe:STATe?')
		return Conversions.str_to_bool(response)

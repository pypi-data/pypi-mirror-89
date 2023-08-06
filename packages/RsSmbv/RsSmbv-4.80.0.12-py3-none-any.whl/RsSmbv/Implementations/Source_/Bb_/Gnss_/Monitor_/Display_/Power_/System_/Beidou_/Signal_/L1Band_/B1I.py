from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class B1I:
	"""B1I commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("b1I", core, parent)

	def set(self, signal_state: bool, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:MONitor<CH>:DISPlay:POWer:SYSTem:BEIDou<ST>:SIGNal:L1Band:B1I \n
		Snippet: driver.source.bb.gnss.monitor.display.power.system.beidou.signal.l1Band.b1I.set(signal_state = False, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Defines the signals to be visualized on the 'Power View' graph. \n
			:param signal_state: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Monitor')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Beidou')"""
		param = Conversions.bool_to_str(signal_state)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:MONitor{channel_cmd_val}:DISPlay:POWer:SYSTem:BEIDou{stream_cmd_val}:SIGNal:L1Band:B1I {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:GNSS:MONitor<CH>:DISPlay:POWer:SYSTem:BEIDou<ST>:SIGNal:L1Band:B1I \n
		Snippet: value: bool = driver.source.bb.gnss.monitor.display.power.system.beidou.signal.l1Band.b1I.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Defines the signals to be visualized on the 'Power View' graph. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Monitor')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Beidou')
			:return: signal_state: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:MONitor{channel_cmd_val}:DISPlay:POWer:SYSTem:BEIDou{stream_cmd_val}:SIGNal:L1Band:B1I?')
		return Conversions.str_to_bool(response)

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Gain:
	"""Gain commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("gain", core, parent)

	def set(self, gain: float, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EVDO:TERMinal<ST>:DCHannel:PACKet<CH>:GAIN \n
		Snippet: driver.source.bb.evdo.terminal.dchannel.packet.gain.set(gain = 1.0, stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		(enabled for an access terminal working in traffic mode) Sets the gain in dB of the Data Channel relative to the pilot
		channel power. Note: Configuration of Packet 2 and Packet 3 transmitted on the second and the third subframe, is only
		enabled for physical layer subtype 2. \n
			:param gain: float Range: -80 to 30
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Packet')"""
		param = Conversions.decimal_value_to_str(gain)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:TERMinal{stream_cmd_val}:DCHannel:PACKet{channel_cmd_val}:GAIN {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:EVDO:TERMinal<ST>:DCHannel:PACKet<CH>:GAIN \n
		Snippet: value: float = driver.source.bb.evdo.terminal.dchannel.packet.gain.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		(enabled for an access terminal working in traffic mode) Sets the gain in dB of the Data Channel relative to the pilot
		channel power. Note: Configuration of Packet 2 and Packet 3 transmitted on the second and the third subframe, is only
		enabled for physical layer subtype 2. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Packet')
			:return: gain: float Range: -80 to 30"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:TERMinal{stream_cmd_val}:DCHannel:PACKet{channel_cmd_val}:GAIN?')
		return Conversions.str_to_float(response)

from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Offset:
	"""Offset commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("offset", core, parent)

	def set(self, power_offset: float, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GPS<ST>:SIGNal:L1Band:P:POWer:OFFset \n
		Snippet: driver.source.bb.gnss.svid.gps.signal.l1Band.p.power.offset.set(power_offset = 1.0, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets a power offset for the selected signal. \n
			:param power_offset: float Range: -6 to 0
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')"""
		param = Conversions.decimal_value_to_str(power_offset)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GPS{stream_cmd_val}:SIGNal:L1Band:P:POWer:OFFset {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GPS<ST>:SIGNal:L1Band:P:POWer:OFFset \n
		Snippet: value: float = driver.source.bb.gnss.svid.gps.signal.l1Band.p.power.offset.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets a power offset for the selected signal. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')
			:return: power_offset: float Range: -6 to 0"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GPS{stream_cmd_val}:SIGNal:L1Band:P:POWer:OFFset?')
		return Conversions.str_to_float(response)

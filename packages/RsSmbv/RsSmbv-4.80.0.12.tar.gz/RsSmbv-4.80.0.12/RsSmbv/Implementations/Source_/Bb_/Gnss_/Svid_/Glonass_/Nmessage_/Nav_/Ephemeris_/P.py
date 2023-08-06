from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class P:
	"""P commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("p", core, parent)

	def set(self, pparam: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GLONass<ST>:NMESsage:NAV:EPHemeris:P \n
		Snippet: driver.source.bb.gnss.svid.glonass.nmessage.nav.ephemeris.p.set(pparam = 1, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the satellite operation mode - P parameter. \n
			:param pparam: integer Range: 0 to 3
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Glonass')"""
		param = Conversions.decimal_value_to_str(pparam)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GLONass{stream_cmd_val}:NMESsage:NAV:EPHemeris:P {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GLONass<ST>:NMESsage:NAV:EPHemeris:P \n
		Snippet: value: int = driver.source.bb.gnss.svid.glonass.nmessage.nav.ephemeris.p.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the satellite operation mode - P parameter. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Glonass')
			:return: pparam: integer Range: 0 to 3"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GLONass{stream_cmd_val}:NMESsage:NAV:EPHemeris:P?')
		return Conversions.str_to_int(response)

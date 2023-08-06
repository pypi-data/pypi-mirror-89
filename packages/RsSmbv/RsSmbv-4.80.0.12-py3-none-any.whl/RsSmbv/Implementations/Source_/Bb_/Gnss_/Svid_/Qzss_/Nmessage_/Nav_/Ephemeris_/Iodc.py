from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Iodc:
	"""Iodc commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("iodc", core, parent)

	def set(self, iodc: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:QZSS<ST>:NMESsage:NAV:EPHemeris:IODC \n
		Snippet: driver.source.bb.gnss.svid.qzss.nmessage.nav.ephemeris.iodc.set(iodc = 1, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the issue of data, clock (IODC) . \n
			:param iodc: integer Range: 0 to 1023
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qzss')"""
		param = Conversions.decimal_value_to_str(iodc)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:QZSS{stream_cmd_val}:NMESsage:NAV:EPHemeris:IODC {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:QZSS<ST>:NMESsage:NAV:EPHemeris:IODC \n
		Snippet: value: int = driver.source.bb.gnss.svid.qzss.nmessage.nav.ephemeris.iodc.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the issue of data, clock (IODC) . \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qzss')
			:return: iodc: integer Range: 0 to 1023"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:QZSS{stream_cmd_val}:NMESsage:NAV:EPHemeris:IODC?')
		return Conversions.str_to_int(response)

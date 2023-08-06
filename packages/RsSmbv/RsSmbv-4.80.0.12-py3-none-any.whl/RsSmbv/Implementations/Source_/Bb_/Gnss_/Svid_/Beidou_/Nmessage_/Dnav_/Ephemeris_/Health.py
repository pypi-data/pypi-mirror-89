from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Health:
	"""Health commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("health", core, parent)

	def set(self, sv_healt: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:BEIDou<ST>:NMESsage:DNAV:EPHemeris:HEALth \n
		Snippet: driver.source.bb.gnss.svid.beidou.nmessage.dnav.ephemeris.health.set(sv_healt = 1, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the SV health. See also method RsSmbv.Source.Bb.Gnss.Svid.Gps.Healthy.set. \n
			:param sv_healt: integer Range: 0 to 63
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Beidou')"""
		param = Conversions.decimal_value_to_str(sv_healt)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:BEIDou{stream_cmd_val}:NMESsage:DNAV:EPHemeris:HEALth {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:BEIDou<ST>:NMESsage:DNAV:EPHemeris:HEALth \n
		Snippet: value: int = driver.source.bb.gnss.svid.beidou.nmessage.dnav.ephemeris.health.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the SV health. See also method RsSmbv.Source.Bb.Gnss.Svid.Gps.Healthy.set. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Beidou')
			:return: sv_healt: integer Range: 0 to 63"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:BEIDou{stream_cmd_val}:NMESsage:DNAV:EPHemeris:HEALth?')
		return Conversions.str_to_int(response)

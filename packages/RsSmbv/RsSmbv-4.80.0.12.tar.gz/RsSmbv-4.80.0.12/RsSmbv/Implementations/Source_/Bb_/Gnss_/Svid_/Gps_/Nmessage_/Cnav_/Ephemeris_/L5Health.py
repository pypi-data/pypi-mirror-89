from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class L5Health:
	"""L5Health commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("l5Health", core, parent)

	def set(self, l_5_health: bool, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GPS<ST>:NMESsage:CNAV:EPHemeris:L5Health \n
		Snippet: driver.source.bb.gnss.svid.gps.nmessage.cnav.ephemeris.l5Health.set(l_5_health = False, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the L1, L2 or L5 health flag in the GPS/QZSS CNAV message. \n
			:param l_5_health: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')"""
		param = Conversions.bool_to_str(l_5_health)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GPS{stream_cmd_val}:NMESsage:CNAV:EPHemeris:L5Health {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GPS<ST>:NMESsage:CNAV:EPHemeris:L5Health \n
		Snippet: value: bool = driver.source.bb.gnss.svid.gps.nmessage.cnav.ephemeris.l5Health.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the L1, L2 or L5 health flag in the GPS/QZSS CNAV message. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')
			:return: l_5_health: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GPS{stream_cmd_val}:NMESsage:CNAV:EPHemeris:L5Health?')
		return Conversions.str_to_bool(response)

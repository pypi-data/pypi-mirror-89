from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ned1:
	"""Ned1 commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ned1", core, parent)

	def set(self, ned_1: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GPS<ST>:NMESsage:CNAV:EPHemeris:NED1 \n
		Snippet: driver.source.bb.gnss.svid.gps.nmessage.cnav.ephemeris.ned1.set(ned_1 = 1, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the NED accuracy index (NED0) , accuracy change indexs (NED1) and accuracy change rate index (NED2) . \n
			:param ned_1: integer Range: 0 to 7
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')"""
		param = Conversions.decimal_value_to_str(ned_1)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GPS{stream_cmd_val}:NMESsage:CNAV:EPHemeris:NED1 {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GPS<ST>:NMESsage:CNAV:EPHemeris:NED1 \n
		Snippet: value: int = driver.source.bb.gnss.svid.gps.nmessage.cnav.ephemeris.ned1.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the NED accuracy index (NED0) , accuracy change indexs (NED1) and accuracy change rate index (NED2) . \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')
			:return: ned_1: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GPS{stream_cmd_val}:NMESsage:CNAV:EPHemeris:NED1?')
		return Conversions.str_to_int(response)

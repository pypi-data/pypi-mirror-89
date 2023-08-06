from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Unscaled:
	"""Unscaled commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("unscaled", core, parent)

	def set(self, isc_l_2_c: float, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GPS<ST>:NMESsage:CNAV:CCORection:ISC:L2C:UNSCaled \n
		Snippet: driver.source.bb.gnss.svid.gps.nmessage.cnav.ccorrection.isc.l2C.unscaled.set(isc_l_2_c = 1.0, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the inter-signal corrections (ISC) parameters of the GPS/QZSS CNAV message. \n
			:param isc_l_2_c: integer Range: -4096 to 4095
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')"""
		param = Conversions.decimal_value_to_str(isc_l_2_c)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GPS{stream_cmd_val}:NMESsage:CNAV:CCORection:ISC:L2C:UNSCaled {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GPS<ST>:NMESsage:CNAV:CCORection:ISC:L2C:UNSCaled \n
		Snippet: value: float = driver.source.bb.gnss.svid.gps.nmessage.cnav.ccorrection.isc.l2C.unscaled.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the inter-signal corrections (ISC) parameters of the GPS/QZSS CNAV message. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')
			:return: isc_l_2_c: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GPS{stream_cmd_val}:NMESsage:CNAV:CCORection:ISC:L2C:UNSCaled?')
		return Conversions.str_to_float(response)

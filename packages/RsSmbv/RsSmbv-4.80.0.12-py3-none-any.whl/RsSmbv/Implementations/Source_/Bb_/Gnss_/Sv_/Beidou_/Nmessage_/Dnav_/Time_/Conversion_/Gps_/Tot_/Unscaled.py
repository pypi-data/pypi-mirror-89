from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal import Conversions
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Unscaled:
	"""Unscaled commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("unscaled", core, parent)

	def set(self, tot: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SV:BEIDou<ST>:NMESsage:DNAV:TIME:CONVersion:GPS<CH>:TOT:UNSCaled \n
		Snippet: driver.source.bb.gnss.sv.beidou.nmessage.dnav.time.conversion.gps.tot.unscaled.set(tot = 1, stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the Tot parameter. \n
			:param tot: integer Range: 0 to 65535
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Beidou')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')"""
		param = Conversions.decimal_value_to_str(tot)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SV:BEIDou{stream_cmd_val}:NMESsage:DNAV:TIME:CONVersion:GPS{channel_cmd_val}:TOT:UNSCaled {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SV:BEIDou<ST>:NMESsage:DNAV:TIME:CONVersion:GPS<CH>:TOT:UNSCaled \n
		Snippet: value: int = driver.source.bb.gnss.sv.beidou.nmessage.dnav.time.conversion.gps.tot.unscaled.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the Tot parameter. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Beidou')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')
			:return: tot: integer Range: 0 to 65535"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SV:BEIDou{stream_cmd_val}:NMESsage:DNAV:TIME:CONVersion:GPS{channel_cmd_val}:TOT:UNSCaled?')
		return Conversions.str_to_int(response)

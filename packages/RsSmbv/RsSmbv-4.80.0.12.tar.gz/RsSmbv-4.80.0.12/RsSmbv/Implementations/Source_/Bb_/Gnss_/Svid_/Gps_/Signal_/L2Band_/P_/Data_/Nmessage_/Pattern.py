from typing import List

from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pattern:
	"""Pattern commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pattern", core, parent)

	def set(self, pattern: List[str], channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GPS<ST>:SIGNal:L2Band:P:DATA:NMESsage:PATTern \n
		Snippet: driver.source.bb.gnss.svid.gps.signal.l2Band.p.data.nmessage.pattern.set(pattern = ['raw1', 'raw2', 'raw3'], channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets a bit pattern as data source. \n
			:param pattern: 64 bits
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')"""
		param = Conversions.list_to_csv_str(pattern)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GPS{stream_cmd_val}:SIGNal:L2Band:P:DATA:NMESsage:PATTern {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GPS<ST>:SIGNal:L2Band:P:DATA:NMESsage:PATTern \n
		Snippet: value: List[str] = driver.source.bb.gnss.svid.gps.signal.l2Band.p.data.nmessage.pattern.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets a bit pattern as data source. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')
			:return: pattern: 64 bits"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GPS{stream_cmd_val}:SIGNal:L2Band:P:DATA:NMESsage:PATTern?')
		return Conversions.str_to_str_list(response)

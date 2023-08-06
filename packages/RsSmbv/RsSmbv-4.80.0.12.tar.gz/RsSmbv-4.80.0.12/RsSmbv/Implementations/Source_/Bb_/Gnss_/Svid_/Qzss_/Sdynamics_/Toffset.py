from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Toffset:
	"""Toffset commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("toffset", core, parent)

	def set(self, time_offset: float, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:QZSS<ST>:SDYNamics:TOFFset \n
		Snippet: driver.source.bb.gnss.svid.qzss.sdynamics.toffset.set(time_offset = 1.0, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets a time delay before the profile is applied. \n
			:param time_offset: float Range: 0 to 9E4
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qzss')"""
		param = Conversions.decimal_value_to_str(time_offset)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:QZSS{stream_cmd_val}:SDYNamics:TOFFset {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:QZSS<ST>:SDYNamics:TOFFset \n
		Snippet: value: float = driver.source.bb.gnss.svid.qzss.sdynamics.toffset.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets a time delay before the profile is applied. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qzss')
			:return: time_offset: float Range: 0 to 9E4"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:QZSS{stream_cmd_val}:SDYNamics:TOFFset?')
		return Conversions.str_to_float(response)

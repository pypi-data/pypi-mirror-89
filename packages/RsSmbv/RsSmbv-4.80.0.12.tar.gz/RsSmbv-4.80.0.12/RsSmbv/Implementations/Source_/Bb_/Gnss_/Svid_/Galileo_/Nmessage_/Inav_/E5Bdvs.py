from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class E5Bdvs:
	"""E5Bdvs commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("e5Bdvs", core, parent)

	def set(self, dvs_e_5_b: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GALileo<ST>:NMESsage:INAV:E5BDVS \n
		Snippet: driver.source.bb.gnss.svid.galileo.nmessage.inav.e5Bdvs.set(dvs_e_5_b = 1, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the data validity status - E5bDVS parameter. \n
			:param dvs_e_5_b: integer Range: -1 to 1
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Galileo')"""
		param = Conversions.decimal_value_to_str(dvs_e_5_b)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GALileo{stream_cmd_val}:NMESsage:INAV:E5BDVS {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GALileo<ST>:NMESsage:INAV:E5BDVS \n
		Snippet: value: int = driver.source.bb.gnss.svid.galileo.nmessage.inav.e5Bdvs.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the data validity status - E5bDVS parameter. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Galileo')
			:return: dvs_e_5_b: integer Range: -1 to 1"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GALileo{stream_cmd_val}:NMESsage:INAV:E5BDVS?')
		return Conversions.str_to_int(response)

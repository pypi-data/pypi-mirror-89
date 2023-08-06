from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Unscaled:
	"""Unscaled commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("unscaled", core, parent)

	def set(self, tgd: float, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:BEIDou<ST>:NMESsage:DNAV:CCORrection:TGD:UNSCaled \n
		Snippet: driver.source.bb.gnss.svid.beidou.nmessage.dnav.ccorrection.tgd.unscaled.set(tgd = 1.0, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the group delay. \n
			:param tgd: integer Range: -128 to 127
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Beidou')"""
		param = Conversions.decimal_value_to_str(tgd)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:BEIDou{stream_cmd_val}:NMESsage:DNAV:CCORrection:TGD:UNSCaled {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:BEIDou<ST>:NMESsage:DNAV:CCORrection:TGD:UNSCaled \n
		Snippet: value: float = driver.source.bb.gnss.svid.beidou.nmessage.dnav.ccorrection.tgd.unscaled.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the group delay. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Beidou')
			:return: tgd: integer Range: -128 to 127"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:BEIDou{stream_cmd_val}:NMESsage:DNAV:CCORrection:TGD:UNSCaled?')
		return Conversions.str_to_float(response)

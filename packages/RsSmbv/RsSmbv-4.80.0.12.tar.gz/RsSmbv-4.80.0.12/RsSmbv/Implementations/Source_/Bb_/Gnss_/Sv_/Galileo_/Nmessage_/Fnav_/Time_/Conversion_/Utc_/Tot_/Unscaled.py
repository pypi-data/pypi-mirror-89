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
		"""SCPI: [SOURce<HW>]:BB:GNSS:SV:GALileo<ST>:NMESsage:FNAV:TIME:CONVersion:UTC<CH>:TOT:UNSCaled \n
		Snippet: driver.source.bb.gnss.sv.galileo.nmessage.fnav.time.conversion.utc.tot.unscaled.set(tot = 1, stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the parameter Tot. \n
			:param tot: integer Range: 0 to 65535
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Galileo')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Utc')"""
		param = Conversions.decimal_value_to_str(tot)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SV:GALileo{stream_cmd_val}:NMESsage:FNAV:TIME:CONVersion:UTC{channel_cmd_val}:TOT:UNSCaled {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SV:GALileo<ST>:NMESsage:FNAV:TIME:CONVersion:UTC<CH>:TOT:UNSCaled \n
		Snippet: value: int = driver.source.bb.gnss.sv.galileo.nmessage.fnav.time.conversion.utc.tot.unscaled.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the parameter Tot. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Galileo')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Utc')
			:return: tot: integer Range: 0 to 65535"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SV:GALileo{stream_cmd_val}:NMESsage:FNAV:TIME:CONVersion:UTC{channel_cmd_val}:TOT:UNSCaled?')
		return Conversions.str_to_int(response)

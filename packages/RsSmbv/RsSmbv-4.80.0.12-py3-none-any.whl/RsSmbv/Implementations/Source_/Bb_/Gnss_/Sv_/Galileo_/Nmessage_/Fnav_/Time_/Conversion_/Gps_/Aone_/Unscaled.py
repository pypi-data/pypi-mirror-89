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

	def set(self, a_1: float, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SV:GALileo<ST>:NMESsage:FNAV:TIME:CONVersion:GPS<CH>:AONE:UNSCaled \n
		Snippet: driver.source.bb.gnss.sv.galileo.nmessage.fnav.time.conversion.gps.aone.unscaled.set(a_1 = 1.0, stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the A1 parameter. \n
			:param a_1: integer Range: -4096 to 4095
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Galileo')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')"""
		param = Conversions.decimal_value_to_str(a_1)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SV:GALileo{stream_cmd_val}:NMESsage:FNAV:TIME:CONVersion:GPS{channel_cmd_val}:AONE:UNSCaled {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SV:GALileo<ST>:NMESsage:FNAV:TIME:CONVersion:GPS<CH>:AONE:UNSCaled \n
		Snippet: value: float = driver.source.bb.gnss.sv.galileo.nmessage.fnav.time.conversion.gps.aone.unscaled.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the A1 parameter. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Galileo')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')
			:return: a_1: integer Range: -4096 to 4095"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SV:GALileo{stream_cmd_val}:NMESsage:FNAV:TIME:CONVersion:GPS{channel_cmd_val}:AONE:UNSCaled?')
		return Conversions.str_to_float(response)

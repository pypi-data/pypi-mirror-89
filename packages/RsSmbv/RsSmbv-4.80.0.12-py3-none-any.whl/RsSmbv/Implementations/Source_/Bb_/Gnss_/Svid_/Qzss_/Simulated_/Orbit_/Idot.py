from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Idot:
	"""Idot commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("idot", core, parent)

	def set(self, idot: float, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:QZSS<ST>:SIMulated:ORBit:IDOT \n
		Snippet: driver.source.bb.gnss.svid.qzss.simulated.orbit.idot.set(idot = 1.0, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the rate of inclination angle. \n
			:param idot: float
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qzss')"""
		param = Conversions.decimal_value_to_str(idot)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:QZSS{stream_cmd_val}:SIMulated:ORBit:IDOT {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:QZSS<ST>:SIMulated:ORBit:IDOT \n
		Snippet: value: float = driver.source.bb.gnss.svid.qzss.simulated.orbit.idot.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the rate of inclination angle. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qzss')
			:return: idot: float"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:QZSS{stream_cmd_val}:SIMulated:ORBit:IDOT?')
		return Conversions.str_to_float(response)

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

	def set(self, omega: float, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:NAVic<ST>:NMESsage:NAV:EPHemeris:OMEGa:UNSCaled \n
		Snippet: driver.source.bb.gnss.svid.navic.nmessage.nav.ephemeris.omega.unscaled.set(omega = 1.0, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the argument of perigee. \n
			:param omega: integer
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Navic')"""
		param = Conversions.decimal_value_to_str(omega)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:NAVic{stream_cmd_val}:NMESsage:NAV:EPHemeris:OMEGa:UNSCaled {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:NAVic<ST>:NMESsage:NAV:EPHemeris:OMEGa:UNSCaled \n
		Snippet: value: float = driver.source.bb.gnss.svid.navic.nmessage.nav.ephemeris.omega.unscaled.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the argument of perigee. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Navic')
			:return: omega: integer"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:NAVic{stream_cmd_val}:NMESsage:NAV:EPHemeris:OMEGa:UNSCaled?')
		return Conversions.str_to_float(response)

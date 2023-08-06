from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ura:
	"""Ura commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ura", core, parent)

	def set(self, ura: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:NAVic<ST>:NMESsage:NAV:EPHemeris:URA \n
		Snippet: driver.source.bb.gnss.svid.navic.nmessage.nav.ephemeris.ura.set(ura = 1, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the user range accuracy index. \n
			:param ura: integer Range: 0 to 15
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Navic')"""
		param = Conversions.decimal_value_to_str(ura)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:NAVic{stream_cmd_val}:NMESsage:NAV:EPHemeris:URA {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:NAVic<ST>:NMESsage:NAV:EPHemeris:URA \n
		Snippet: value: int = driver.source.bb.gnss.svid.navic.nmessage.nav.ephemeris.ura.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the user range accuracy index. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Navic')
			:return: ura: integer Range: 0 to 15"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:NAVic{stream_cmd_val}:NMESsage:NAV:EPHemeris:URA?')
		return Conversions.str_to_int(response)

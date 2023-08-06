from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Shealth:
	"""Shealth commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("shealth", core, parent)

	def set(self, shealth: bool, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:NAVic<ST>:NMESsage:NAV:EPHemeris:SHEalth \n
		Snippet: driver.source.bb.gnss.svid.navic.nmessage.nav.ephemeris.shealth.set(shealth = False, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the S health. \n
			:param shealth: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Navic')"""
		param = Conversions.bool_to_str(shealth)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:NAVic{stream_cmd_val}:NMESsage:NAV:EPHemeris:SHEalth {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:NAVic<ST>:NMESsage:NAV:EPHemeris:SHEalth \n
		Snippet: value: bool = driver.source.bb.gnss.svid.navic.nmessage.nav.ephemeris.shealth.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the S health. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Navic')
			:return: shealth: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:NAVic{stream_cmd_val}:NMESsage:NAV:EPHemeris:SHEalth?')
		return Conversions.str_to_bool(response)

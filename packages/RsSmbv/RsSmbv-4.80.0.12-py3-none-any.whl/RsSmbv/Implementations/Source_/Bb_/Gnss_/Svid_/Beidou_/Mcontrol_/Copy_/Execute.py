from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Execute:
	"""Execute commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("execute", core, parent)

	def set(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:BEIDou<ST>:MCONtrol:COPY:EXECute \n
		Snippet: driver.source.bb.gnss.svid.beidou.mcontrol.copy.execute.set(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Applies the configuration of the current satellite (SVID<ch>:<GNSS system>) to the satellite defined with the command
		method RsSmbv.Source.Bb.Gnss.Svid.Gps.Mcontrol.Copy.Svid.set. Both SV IDs belong to the same GNSS system. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Beidou')"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:BEIDou{stream_cmd_val}:MCONtrol:COPY:EXECute')

	def set_with_opc(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:BEIDou<ST>:MCONtrol:COPY:EXECute \n
		Snippet: driver.source.bb.gnss.svid.beidou.mcontrol.copy.execute.set_with_opc(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Applies the configuration of the current satellite (SVID<ch>:<GNSS system>) to the satellite defined with the command
		method RsSmbv.Source.Bb.Gnss.Svid.Gps.Mcontrol.Copy.Svid.set. Both SV IDs belong to the same GNSS system. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Beidou')"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:BEIDou{stream_cmd_val}:MCONtrol:COPY:EXECute')

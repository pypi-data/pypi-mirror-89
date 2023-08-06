from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Append:
	"""Append commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("append", core, parent)

	def set(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GPS<ST>:PRERrors:PROFile:APPend \n
		Snippet: driver.source.bb.gnss.svid.gps.prErrors.profile.append.set(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Appends a row in the profile table. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GPS{stream_cmd_val}:PRERrors:PROFile:APPend')

	def set_with_opc(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GPS<ST>:PRERrors:PROFile:APPend \n
		Snippet: driver.source.bb.gnss.svid.gps.prErrors.profile.append.set_with_opc(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Appends a row in the profile table. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GPS{stream_cmd_val}:PRERrors:PROFile:APPend')

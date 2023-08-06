from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............Internal.Utilities import trim_str_response
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dselect:
	"""Dselect commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dselect", core, parent)

	def set(self, dselect: str, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:BEIDou<ST>:SIGNal:L5Band:B2I:DATA:NMESsage:DSELect \n
		Snippet: driver.source.bb.gnss.svid.beidou.signal.l5Band.b2I.data.nmessage.dselect.set(dselect = '1', channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Selects an existing data list file from the default directory or from the specific directory. Refer to 'Accessing Files
		in the Default or Specified Directory' for general information on file handling in the default and in a specific
		directory. \n
			:param dselect: string Filename incl. file extension or complete file path
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Beidou')"""
		param = Conversions.value_to_quoted_str(dselect)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:BEIDou{stream_cmd_val}:SIGNal:L5Band:B2I:DATA:NMESsage:DSELect {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:BEIDou<ST>:SIGNal:L5Band:B2I:DATA:NMESsage:DSELect \n
		Snippet: value: str = driver.source.bb.gnss.svid.beidou.signal.l5Band.b2I.data.nmessage.dselect.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Selects an existing data list file from the default directory or from the specific directory. Refer to 'Accessing Files
		in the Default or Specified Directory' for general information on file handling in the default and in a specific
		directory. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Beidou')
			:return: dselect: string Filename incl. file extension or complete file path"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:BEIDou{stream_cmd_val}:SIGNal:L5Band:B2I:DATA:NMESsage:DSELect?')
		return trim_str_response(response)

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StsFrame:
	"""StsFrame commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("stsFrame", core, parent)

	def set(self, starting_sf: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:LAA:CELL<CH>:BURSt<ST>:STSFrame \n
		Snippet: driver.source.bb.eutra.dl.laa.cell.burst.stsFrame.set(starting_sf = 1, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the first subframe of the LAA bust. \n
			:param starting_sf: integer Range: 0 to 39
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Burst')"""
		param = Conversions.decimal_value_to_str(starting_sf)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:LAA:CELL{channel_cmd_val}:BURSt{stream_cmd_val}:STSFrame {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:LAA:CELL<CH>:BURSt<ST>:STSFrame \n
		Snippet: value: int = driver.source.bb.eutra.dl.laa.cell.burst.stsFrame.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the first subframe of the LAA bust. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Burst')
			:return: starting_sf: integer Range: 0 to 39"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:LAA:CELL{channel_cmd_val}:BURSt{stream_cmd_val}:STSFrame?')
		return Conversions.str_to_int(response)

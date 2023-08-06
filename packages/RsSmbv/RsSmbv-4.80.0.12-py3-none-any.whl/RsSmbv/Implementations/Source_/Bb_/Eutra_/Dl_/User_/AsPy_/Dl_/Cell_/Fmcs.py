from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fmcs:
	"""Fmcs commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fmcs", core, parent)

	def set(self, fixed_mcs: int, channel=repcap.Channel.Default, stream=repcap.Stream.Nr1) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:USER<CH>:AS:DL:CELL<ST>:FMCS \n
		Snippet: driver.source.bb.eutra.dl.user.asPy.dl.cell.fmcs.set(fixed_mcs = 1, channel = repcap.Channel.Default, stream = repcap.Stream.Nr1) \n
		Sets the MCS value. \n
			:param fixed_mcs: integer Range: 0 to 31
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1"""
		param = Conversions.decimal_value_to_str(fixed_mcs)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:AS:DL:CELL{stream_cmd_val}:FMCS {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Nr1) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:USER<CH>:AS:DL:CELL<ST>:FMCS \n
		Snippet: value: int = driver.source.bb.eutra.dl.user.asPy.dl.cell.fmcs.get(channel = repcap.Channel.Default, stream = repcap.Stream.Nr1) \n
		Sets the MCS value. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1
			:return: fixed_mcs: integer Range: 0 to 31"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:AS:DL:CELL{stream_cmd_val}:FMCS?')
		return Conversions.str_to_int(response)

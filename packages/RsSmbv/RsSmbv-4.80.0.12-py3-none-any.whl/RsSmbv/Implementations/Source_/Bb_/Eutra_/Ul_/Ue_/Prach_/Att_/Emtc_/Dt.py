from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dt:
	"""Dt commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dt", core, parent)

	def set(self, delta_time: float, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:PRACh:ATT<CH>:EMTC:DT \n
		Snippet: driver.source.bb.eutra.ul.ue.prach.att.emtc.dt.set(delta_time = 1.0, stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the parameter Delta_t in us. \n
			:param delta_time: float Range: -500 to 500
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Att')"""
		param = Conversions.decimal_value_to_str(delta_time)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:PRACh:ATT{channel_cmd_val}:EMTC:DT {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:PRACh:ATT<CH>:EMTC:DT \n
		Snippet: value: float = driver.source.bb.eutra.ul.ue.prach.att.emtc.dt.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the parameter Delta_t in us. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Att')
			:return: delta_time: float Range: -500 to 500"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:PRACh:ATT{channel_cmd_val}:EMTC:DT?')
		return Conversions.str_to_float(response)

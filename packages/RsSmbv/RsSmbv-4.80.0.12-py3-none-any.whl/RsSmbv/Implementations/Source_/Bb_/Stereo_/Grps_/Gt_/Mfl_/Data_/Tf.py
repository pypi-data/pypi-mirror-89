from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tf:
	"""Tf commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tf", core, parent)

	def set(self, tf: float, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:STEReo:GRPS:GT<ST>:MFL:DATA<CH>:TF \n
		Snippet: driver.source.bb.stereo.grps.gt.mfl.data.tf.set(tf = 1.0, stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		No command help available \n
			:param tf: No help available
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gt')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Data')"""
		param = Conversions.decimal_value_to_str(tf)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:GRPS:GT{stream_cmd_val}:MFL:DATA{channel_cmd_val}:TF {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:STEReo:GRPS:GT<ST>:MFL:DATA<CH>:TF \n
		Snippet: value: float = driver.source.bb.stereo.grps.gt.mfl.data.tf.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		No command help available \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gt')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Data')
			:return: tf: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:STEReo:GRPS:GT{stream_cmd_val}:MFL:DATA{channel_cmd_val}:TF?')
		return Conversions.str_to_float(response)

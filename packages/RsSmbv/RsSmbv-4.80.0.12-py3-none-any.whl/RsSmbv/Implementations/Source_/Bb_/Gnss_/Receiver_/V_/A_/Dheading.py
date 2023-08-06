from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dheading:
	"""Dheading commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dheading", core, parent)

	def set(self, delta_heading: float, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:A<CH>:DHEading \n
		Snippet: driver.source.bb.gnss.receiver.v.a.dheading.set(delta_heading = 1.0, stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the antenna orientation and tilt. The values are set relative to the center of gravity (COG) . \n
			:param delta_heading: float Range: -180 to 180
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'A')"""
		param = Conversions.decimal_value_to_str(delta_heading)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:A{channel_cmd_val}:DHEading {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:A<CH>:DHEading \n
		Snippet: value: float = driver.source.bb.gnss.receiver.v.a.dheading.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the antenna orientation and tilt. The values are set relative to the center of gravity (COG) . \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'A')
			:return: delta_heading: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:A{channel_cmd_val}:DHEading?')
		return Conversions.str_to_float(response)

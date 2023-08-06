from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ivelocity:
	"""Ivelocity commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ivelocity", core, parent)

	def set(self, initial_velocity: float, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GPS<ST>:SDYNamics:IVELocity \n
		Snippet: driver.source.bb.gnss.svid.gps.sdynamics.ivelocity.set(initial_velocity = 1.0, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Indicates the initial velocity, used at the beginning of the profile. \n
			:param initial_velocity: float Range: -19042 to 19042
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')"""
		param = Conversions.decimal_value_to_str(initial_velocity)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GPS{stream_cmd_val}:SDYNamics:IVELocity {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GPS<ST>:SDYNamics:IVELocity \n
		Snippet: value: float = driver.source.bb.gnss.svid.gps.sdynamics.ivelocity.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Indicates the initial velocity, used at the beginning of the profile. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')
			:return: initial_velocity: float Range: -19042 to 19042"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GPS{stream_cmd_val}:SDYNamics:IVELocity?')
		return Conversions.str_to_float(response)

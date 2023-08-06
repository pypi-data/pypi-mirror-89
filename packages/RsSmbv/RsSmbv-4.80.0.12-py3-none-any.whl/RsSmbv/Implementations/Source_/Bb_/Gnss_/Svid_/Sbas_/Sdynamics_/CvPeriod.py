from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CvPeriod:
	"""CvPeriod commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cvPeriod", core, parent)

	def set(self, const_vel_period: float, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:SBAS<ST>:SDYNamics:CVPeriod \n
		Snippet: driver.source.bb.gnss.svid.sbas.sdynamics.cvPeriod.set(const_vel_period = 1.0, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the time period during that the velocity is kept constant. \n
			:param const_vel_period: float Range: 0.1 to 10800
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbas')"""
		param = Conversions.decimal_value_to_str(const_vel_period)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:SBAS{stream_cmd_val}:SDYNamics:CVPeriod {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:SBAS<ST>:SDYNamics:CVPeriod \n
		Snippet: value: float = driver.source.bb.gnss.svid.sbas.sdynamics.cvPeriod.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the time period during that the velocity is kept constant. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbas')
			:return: const_vel_period: float Range: 0.1 to 10800"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:SBAS{stream_cmd_val}:SDYNamics:CVPeriod?')
		return Conversions.str_to_float(response)

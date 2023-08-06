from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, state: bool, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:SCH:M1T<ST>:LPAir:STATe \n
		Snippet: driver.source.bb.gbas.vdb.sch.m1T.lpair.state.set(state = False, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		If enabled, the set of measurement blocks is included in a linked pair of messages instead in a single message. \n
			:param state: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'M1T')"""
		param = Conversions.bool_to_str(state)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:SCH:M1T{stream_cmd_val}:LPAir:STATe {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:SCH:M1T<ST>:LPAir:STATe \n
		Snippet: value: bool = driver.source.bb.gbas.vdb.sch.m1T.lpair.state.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		If enabled, the set of measurement blocks is included in a linked pair of messages instead in a single message. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'M1T')
			:return: state: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:SCH:M1T{stream_cmd_val}:LPAir:STATe?')
		return Conversions.str_to_bool(response)

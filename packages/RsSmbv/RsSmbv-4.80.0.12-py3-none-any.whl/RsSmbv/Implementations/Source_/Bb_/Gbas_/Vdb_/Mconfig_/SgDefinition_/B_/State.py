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
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:SGDefinition:B<ST>:STATe \n
		Snippet: driver.source.bb.gbas.vdb.mconfig.sgDefinition.b.state.set(state = False, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		If enabled, the specified slot is assigned for use by the ground station. \n
			:param state: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'B')"""
		param = Conversions.bool_to_str(state)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:SGDefinition:B{stream_cmd_val}:STATe {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:SGDefinition:B<ST>:STATe \n
		Snippet: value: bool = driver.source.bb.gbas.vdb.mconfig.sgDefinition.b.state.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		If enabled, the specified slot is assigned for use by the ground station. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'B')
			:return: state: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:SGDefinition:B{stream_cmd_val}:STATe?')
		return Conversions.str_to_bool(response)

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, state: bool, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: SCONfiguration:OUTPut:MAPPing:DIGital<CH>:STReam<ST>:STATe \n
		Snippet: driver.sconfiguration.output.mapping.digital.stream.state.set(state = False, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Maps the I/Q output streams to the output connectors. \n
			:param state: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Digital')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Stream')"""
		param = Conversions.bool_to_str(state)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SCONfiguration:OUTPut:MAPPing:DIGital{channel_cmd_val}:STReam{stream_cmd_val}:STATe {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> bool:
		"""SCPI: SCONfiguration:OUTPut:MAPPing:DIGital<CH>:STReam<ST>:STATe \n
		Snippet: value: bool = driver.sconfiguration.output.mapping.digital.stream.state.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Maps the I/Q output streams to the output connectors. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Digital')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Stream')
			:return: state: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SCONfiguration:OUTPut:MAPPing:DIGital{channel_cmd_val}:STReam{stream_cmd_val}:STATe?')
		return Conversions.str_to_bool(response)

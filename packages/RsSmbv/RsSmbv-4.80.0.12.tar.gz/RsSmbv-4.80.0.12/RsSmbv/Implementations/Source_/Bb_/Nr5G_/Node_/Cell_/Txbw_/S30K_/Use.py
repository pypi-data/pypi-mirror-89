from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Use:
	"""Use commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("use", core, parent)

	def set(self, scs_use: bool, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:TXBW:S30K<ST>:USE \n
		Snippet: driver.source.bb.nr5G.node.cell.txbw.s30K.use.set(scs_use = False, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Enables an SCS in the particular cell. \n
			:param scs_use: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'S30K')"""
		param = Conversions.bool_to_str(scs_use)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:TXBW:S30K{stream_cmd_val}:USE {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:TXBW:S30K<ST>:USE \n
		Snippet: value: bool = driver.source.bb.nr5G.node.cell.txbw.s30K.use.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Enables an SCS in the particular cell. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'S30K')
			:return: scs_use: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:TXBW:S30K{stream_cmd_val}:USE?')
		return Conversions.str_to_bool(response)

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

	def set(self, state: bool, stream=repcap.Stream.Default, channel=repcap.Channel.Default, subchannel=repcap.Subchannel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:UP:CELL<ST>:SLOT<CH>:CHANnel<US>:STATe \n
		Snippet: driver.source.bb.tdscdma.up.cell.slot.channel.state.set(state = False, stream = repcap.Stream.Default, channel = repcap.Channel.Default, subchannel = repcap.Subchannel.Default) \n
		Activates or deactivates the channel. \n
			:param state: 0| 1| OFF| ON
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Slot')
			:param subchannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.bool_to_str(state)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		subchannel_cmd_val = self._base.get_repcap_cmd_value(subchannel, repcap.Subchannel)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:UP:CELL{stream_cmd_val}:SLOT{channel_cmd_val}:CHANnel{subchannel_cmd_val}:STATe {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default, subchannel=repcap.Subchannel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:UP:CELL<ST>:SLOT<CH>:CHANnel<US>:STATe \n
		Snippet: value: bool = driver.source.bb.tdscdma.up.cell.slot.channel.state.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default, subchannel = repcap.Subchannel.Default) \n
		Activates or deactivates the channel. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Slot')
			:param subchannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: state: 0| 1| OFF| ON"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		subchannel_cmd_val = self._base.get_repcap_cmd_value(subchannel, repcap.Subchannel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:UP:CELL{stream_cmd_val}:SLOT{channel_cmd_val}:CHANnel{subchannel_cmd_val}:STATe?')
		return Conversions.str_to_bool(response)

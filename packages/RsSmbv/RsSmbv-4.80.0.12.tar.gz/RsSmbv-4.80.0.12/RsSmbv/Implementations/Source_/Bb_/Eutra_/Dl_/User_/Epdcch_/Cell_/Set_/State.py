from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, state: bool, channel=repcap.Channel.Default, stream=repcap.Stream.Default, direction=repcap.Direction.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:USER<CH>:EPDCch:CELL<ST>:SET<DIR>:STATe \n
		Snippet: driver.source.bb.eutra.dl.user.epdcch.cell.set.state.set(state = False, channel = repcap.Channel.Default, stream = repcap.Stream.Default, direction = repcap.Direction.Default) \n
		Enables the EPDCCH set. \n
			:param state: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param direction: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Set')"""
		param = Conversions.bool_to_str(state)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		direction_cmd_val = self._base.get_repcap_cmd_value(direction, repcap.Direction)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:EPDCch:CELL{stream_cmd_val}:SET{direction_cmd_val}:STATe {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, direction=repcap.Direction.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:USER<CH>:EPDCch:CELL<ST>:SET<DIR>:STATe \n
		Snippet: value: bool = driver.source.bb.eutra.dl.user.epdcch.cell.set.state.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default, direction = repcap.Direction.Default) \n
		Enables the EPDCCH set. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param direction: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Set')
			:return: state: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		direction_cmd_val = self._base.get_repcap_cmd_value(direction, repcap.Direction)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:EPDCch:CELL{stream_cmd_val}:SET{direction_cmd_val}:STATe?')
		return Conversions.str_to_bool(response)

from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class User:
	"""User commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("user", core, parent)

	def set(self, user: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:UP:CELL<ST>:SLOT<CH>:PRAC:MSG:USER \n
		Snippet: driver.source.bb.tdscdma.up.cell.slot.prac.msg.user.set(user = 1, stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets user number. \n
			:param user: integer Range: 1 to 16
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Slot')"""
		param = Conversions.decimal_value_to_str(user)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:UP:CELL{stream_cmd_val}:SLOT{channel_cmd_val}:PRAC:MSG:USER {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:UP:CELL<ST>:SLOT<CH>:PRAC:MSG:USER \n
		Snippet: value: int = driver.source.bb.tdscdma.up.cell.slot.prac.msg.user.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets user number. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Slot')
			:return: user: integer Range: 1 to 16"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:UP:CELL{stream_cmd_val}:SLOT{channel_cmd_val}:PRAC:MSG:USER?')
		return Conversions.str_to_int(response)

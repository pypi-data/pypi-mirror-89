from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Repetition:
	"""Repetition commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("repetition", core, parent)

	def set(self, repetition: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default, subchannel=repcap.Subchannel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:SLOT<CH>:CHANnel<US>:DPCCh:SYNC:REPetition \n
		Snippet: driver.source.bb.tdscdma.down.cell.slot.channel.dpcch.sync.repetition.set(repetition = 1, stream = repcap.Stream.Default, channel = repcap.Channel.Default, subchannel = repcap.Subchannel.Default) \n
		Sets the value for the sync shift repetition. \n
			:param repetition: integer Range: 1 to 8
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Slot')
			:param subchannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.decimal_value_to_str(repetition)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		subchannel_cmd_val = self._base.get_repcap_cmd_value(subchannel, repcap.Subchannel)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:SLOT{channel_cmd_val}:CHANnel{subchannel_cmd_val}:DPCCh:SYNC:REPetition {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default, subchannel=repcap.Subchannel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:SLOT<CH>:CHANnel<US>:DPCCh:SYNC:REPetition \n
		Snippet: value: int = driver.source.bb.tdscdma.down.cell.slot.channel.dpcch.sync.repetition.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default, subchannel = repcap.Subchannel.Default) \n
		Sets the value for the sync shift repetition. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Slot')
			:param subchannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: repetition: integer Range: 1 to 8"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		subchannel_cmd_val = self._base.get_repcap_cmd_value(subchannel, repcap.Subchannel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:SLOT{channel_cmd_val}:CHANnel{subchannel_cmd_val}:DPCCh:SYNC:REPetition?')
		return Conversions.str_to_int(response)

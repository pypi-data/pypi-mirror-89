from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tfci:
	"""Tfci commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tfci", core, parent)

	def set(self, tfci: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default, subchannel=repcap.Subchannel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:UP:CELL<ST>:SLOT<CH>:CHANnel<US>:DPCCh:EUCC:TFCI \n
		Snippet: driver.source.bb.tdscdma.up.cell.slot.channel.dpcch.eucc.tfci.set(tfci = 1, stream = repcap.Stream.Default, channel = repcap.Channel.Default, subchannel = repcap.Subchannel.Default) \n
		Enters the value of the TFCI field. \n
			:param tfci: integer Range: 0 to 63
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Slot')
			:param subchannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.decimal_value_to_str(tfci)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		subchannel_cmd_val = self._base.get_repcap_cmd_value(subchannel, repcap.Subchannel)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:UP:CELL{stream_cmd_val}:SLOT{channel_cmd_val}:CHANnel{subchannel_cmd_val}:DPCCh:EUCC:TFCI {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default, subchannel=repcap.Subchannel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:UP:CELL<ST>:SLOT<CH>:CHANnel<US>:DPCCh:EUCC:TFCI \n
		Snippet: value: int = driver.source.bb.tdscdma.up.cell.slot.channel.dpcch.eucc.tfci.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default, subchannel = repcap.Subchannel.Default) \n
		Enters the value of the TFCI field. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Slot')
			:param subchannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: tfci: integer Range: 0 to 63"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		subchannel_cmd_val = self._base.get_repcap_cmd_value(subchannel, repcap.Subchannel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:UP:CELL{stream_cmd_val}:SLOT{channel_cmd_val}:CHANnel{subchannel_cmd_val}:DPCCh:EUCC:TFCI?')
		return Conversions.str_to_int(response)

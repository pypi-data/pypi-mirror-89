from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tfci:
	"""Tfci commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tfci", core, parent)

	def set(self, tfci: float, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:DPCCh:POFFset:TFCI \n
		Snippet: driver.source.bb.w3Gpp.bstation.channel.dpcch.poffset.tfci.set(tfci = 1.0, stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		The command sets an offset to the set channel power for the TFCI field. \n
			:param tfci: float Range: -10 to 10
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.decimal_value_to_str(tfci)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:DPCCh:POFFset:TFCI {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:DPCCh:POFFset:TFCI \n
		Snippet: value: float = driver.source.bb.w3Gpp.bstation.channel.dpcch.poffset.tfci.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		The command sets an offset to the set channel power for the TFCI field. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: tfci: float Range: -10 to 10"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:DPCCh:POFFset:TFCI?')
		return Conversions.str_to_float(response)

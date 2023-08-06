from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Interleaver:
	"""Interleaver commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("interleaver", core, parent)

	def set(self, interleaver: bool, transportChannel=repcap.TransportChannel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation:ENHanced:DPDCh:TCHannel<DI>:INTerleaver \n
		Snippet: driver.source.bb.w3Gpp.mstation.enhanced.dpdch.tchannel.interleaver.set(interleaver = False, transportChannel = repcap.TransportChannel.Default) \n
		The command activates or deactivates channel coding interleaver state 1 for the selected channel. Interleaver state 1 can
		be activated and deactivated for each channel individually. The channel is selected via the suffix at TCHannel.
		Interleaver state 2 can only be activated or deactivated for all the channels together (method RsSmbv.Source.Bb.W3Gpp.
		Mstation.Enhanced.Dpdch.interleaver2) . \n
			:param interleaver: 0| 1| OFF| ON
			:param transportChannel: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tchannel')"""
		param = Conversions.bool_to_str(interleaver)
		transportChannel_cmd_val = self._base.get_repcap_cmd_value(transportChannel, repcap.TransportChannel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:TCHannel{transportChannel_cmd_val}:INTerleaver {param}')

	def get(self, transportChannel=repcap.TransportChannel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation:ENHanced:DPDCh:TCHannel<DI>:INTerleaver \n
		Snippet: value: bool = driver.source.bb.w3Gpp.mstation.enhanced.dpdch.tchannel.interleaver.get(transportChannel = repcap.TransportChannel.Default) \n
		The command activates or deactivates channel coding interleaver state 1 for the selected channel. Interleaver state 1 can
		be activated and deactivated for each channel individually. The channel is selected via the suffix at TCHannel.
		Interleaver state 2 can only be activated or deactivated for all the channels together (method RsSmbv.Source.Bb.W3Gpp.
		Mstation.Enhanced.Dpdch.interleaver2) . \n
			:param transportChannel: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tchannel')
			:return: interleaver: 0| 1| OFF| ON"""
		transportChannel_cmd_val = self._base.get_repcap_cmd_value(transportChannel, repcap.TransportChannel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:TCHannel{transportChannel_cmd_val}:INTerleaver?')
		return Conversions.str_to_bool(response)

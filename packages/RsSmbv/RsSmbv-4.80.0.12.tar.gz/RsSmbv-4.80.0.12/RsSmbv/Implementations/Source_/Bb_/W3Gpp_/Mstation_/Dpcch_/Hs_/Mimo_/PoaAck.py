from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PoaAck:
	"""PoaAck commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("poaAck", core, parent)

	def set(self, poa_ack: float, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:HS:MIMO:POAAck \n
		Snippet: driver.source.bb.w3Gpp.mstation.dpcch.hs.mimo.poaAck.set(poa_ack = 1.0, stream = repcap.Stream.Default) \n
		(up to Release 7) Sets the power offset Poff_ACK/ACK of an ACK/ACK response to two scheduled transport blocks relative to
		the CQI Power PCQI (method RsSmbv.Source.Bb.W3Gpp.Mstation.Dpcch.Hs.Power.set) . The power PACK/ACK used during the
		HARQ-ACK slots is calculated as: PACK/ACK = PCQI + Poff_ACK/ACK \n
			:param poa_ack: float Range: -10 to 10
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.decimal_value_to_str(poa_ack)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:HS:MIMO:POAAck {param}')

	def get(self, stream=repcap.Stream.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:HS:MIMO:POAAck \n
		Snippet: value: float = driver.source.bb.w3Gpp.mstation.dpcch.hs.mimo.poaAck.get(stream = repcap.Stream.Default) \n
		(up to Release 7) Sets the power offset Poff_ACK/ACK of an ACK/ACK response to two scheduled transport blocks relative to
		the CQI Power PCQI (method RsSmbv.Source.Bb.W3Gpp.Mstation.Dpcch.Hs.Power.set) . The power PACK/ACK used during the
		HARQ-ACK slots is calculated as: PACK/ACK = PCQI + Poff_ACK/ACK \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: poa_ack: float Range: -10 to 10"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:HS:MIMO:POAAck?')
		return Conversions.str_to_float(response)

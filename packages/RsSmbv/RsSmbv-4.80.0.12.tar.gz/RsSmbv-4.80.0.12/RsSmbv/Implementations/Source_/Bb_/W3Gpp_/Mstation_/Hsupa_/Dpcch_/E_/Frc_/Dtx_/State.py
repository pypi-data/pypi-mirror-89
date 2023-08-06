from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, state: bool, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:[HSUPa]:DPCCh:E:FRC:DTX:STATe \n
		Snippet: driver.source.bb.w3Gpp.mstation.hsupa.dpcch.e.frc.dtx.state.set(state = False, stream = repcap.Stream.Default) \n
		The command activates or deactivates the DTX (Discontinuous Transmission) mode. \n
			:param state: ON| OFF
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.bool_to_str(state)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:HSUPa:DPCCh:E:FRC:DTX:STATe {param}')

	def get(self, stream=repcap.Stream.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:[HSUPa]:DPCCh:E:FRC:DTX:STATe \n
		Snippet: value: bool = driver.source.bb.w3Gpp.mstation.hsupa.dpcch.e.frc.dtx.state.get(stream = repcap.Stream.Default) \n
		The command activates or deactivates the DTX (Discontinuous Transmission) mode. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: state: ON| OFF"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:HSUPa:DPCCh:E:FRC:DTX:STATe?')
		return Conversions.str_to_bool(response)

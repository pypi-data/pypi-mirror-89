from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pstep:
	"""Pstep commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pstep", core, parent)

	def set(self, pstep: float, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:C2K:MSTation<ST>:TPC:PSTep \n
		Snippet: driver.source.bb.c2K.mstation.tpc.pstep.set(pstep = 1.0, stream = repcap.Stream.Default) \n
		The command defines the step width for the change of channel powers in the case of 'mis-' use of the power control bits. \n
			:param pstep: float Range: -10 to 10 dB
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.decimal_value_to_str(pstep)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:MSTation{stream_cmd_val}:TPC:PSTep {param}')

	def get(self, stream=repcap.Stream.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:C2K:MSTation<ST>:TPC:PSTep \n
		Snippet: value: float = driver.source.bb.c2K.mstation.tpc.pstep.get(stream = repcap.Stream.Default) \n
		The command defines the step width for the change of channel powers in the case of 'mis-' use of the power control bits. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: pstep: float Range: -10 to 10 dB"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:C2K:MSTation{stream_cmd_val}:TPC:PSTep?')
		return Conversions.str_to_float(response)

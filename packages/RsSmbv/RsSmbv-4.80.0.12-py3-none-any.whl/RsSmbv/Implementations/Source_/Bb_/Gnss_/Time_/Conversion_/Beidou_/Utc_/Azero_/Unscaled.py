from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Unscaled:
	"""Unscaled commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("unscaled", core, parent)

	def set(self, a_0: float, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TIME:CONVersion:BEIDou<ST>:UTC:AZERo:UNSCaled \n
		Snippet: driver.source.bb.gnss.time.conversion.beidou.utc.azero.unscaled.set(a_0 = 1.0, stream = repcap.Stream.Default) \n
		Sets the constant term of polynomial, A0. \n
			:param a_0: integer Range: -2147483648 to 2147483647
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Beidou')"""
		param = Conversions.decimal_value_to_str(a_0)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:TIME:CONVersion:BEIDou{stream_cmd_val}:UTC:AZERo:UNSCaled {param}')

	def get(self, stream=repcap.Stream.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TIME:CONVersion:BEIDou<ST>:UTC:AZERo:UNSCaled \n
		Snippet: value: float = driver.source.bb.gnss.time.conversion.beidou.utc.azero.unscaled.get(stream = repcap.Stream.Default) \n
		Sets the constant term of polynomial, A0. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Beidou')
			:return: a_0: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:TIME:CONVersion:BEIDou{stream_cmd_val}:UTC:AZERo:UNSCaled?')
		return Conversions.str_to_float(response)

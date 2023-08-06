from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Wnot:
	"""Wnot commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("wnot", core, parent)

	def set(self, wnot: int, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TIME:CONVersion:GPS<ST>:UTC:WNOT \n
		Snippet: driver.source.bb.gnss.time.conversion.gps.utc.wnot.set(wnot = 1, stream = repcap.Stream.Default) \n
		Sets the UTC data reference week number, WNt. \n
			:param wnot: integer Range: 0 to 255
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')"""
		param = Conversions.decimal_value_to_str(wnot)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:TIME:CONVersion:GPS{stream_cmd_val}:UTC:WNOT {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TIME:CONVersion:GPS<ST>:UTC:WNOT \n
		Snippet: value: int = driver.source.bb.gnss.time.conversion.gps.utc.wnot.get(stream = repcap.Stream.Default) \n
		Sets the UTC data reference week number, WNt. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')
			:return: wnot: integer Range: 0 to 255"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:TIME:CONVersion:GPS{stream_cmd_val}:UTC:WNOT?')
		return Conversions.str_to_int(response)

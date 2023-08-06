from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rbid:
	"""Rbid commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rbid", core, parent)

	def set(self, rb_index: int, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:PRACh:NIOT:RBID \n
		Snippet: driver.source.bb.eutra.ul.ue.prach.niot.rbid.set(rb_index = 1, stream = repcap.Stream.Default) \n
		Sets the resource block in that the NPRACH is allocated. \n
			:param rb_index: integer Range: 0 to 100
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')"""
		param = Conversions.decimal_value_to_str(rb_index)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:PRACh:NIOT:RBID {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:PRACh:NIOT:RBID \n
		Snippet: value: int = driver.source.bb.eutra.ul.ue.prach.niot.rbid.get(stream = repcap.Stream.Default) \n
		Sets the resource block in that the NPRACH is allocated. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: rb_index: integer Range: 0 to 100"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:PRACh:NIOT:RBID?')
		return Conversions.str_to_int(response)

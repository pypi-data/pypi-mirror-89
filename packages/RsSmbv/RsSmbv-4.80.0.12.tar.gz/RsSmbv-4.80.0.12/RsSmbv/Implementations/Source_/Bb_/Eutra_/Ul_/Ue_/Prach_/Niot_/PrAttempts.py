from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PrAttempts:
	"""PrAttempts commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("prAttempts", core, parent)

	def set(self, preamble_attempt: int, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:PRACh:NIOT:PRATtempts \n
		Snippet: driver.source.bb.eutra.ul.ue.prach.niot.prAttempts.set(preamble_attempt = 1, stream = repcap.Stream.Default) \n
		Sets the number of preamble attempts. \n
			:param preamble_attempt: integer Range: 0 to 30
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')"""
		param = Conversions.decimal_value_to_str(preamble_attempt)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:PRACh:NIOT:PRATtempts {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:PRACh:NIOT:PRATtempts \n
		Snippet: value: int = driver.source.bb.eutra.ul.ue.prach.niot.prAttempts.get(stream = repcap.Stream.Default) \n
		Sets the number of preamble attempts. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: preamble_attempt: integer Range: 0 to 30"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:PRACh:NIOT:PRATtempts?')
		return Conversions.str_to_int(response)

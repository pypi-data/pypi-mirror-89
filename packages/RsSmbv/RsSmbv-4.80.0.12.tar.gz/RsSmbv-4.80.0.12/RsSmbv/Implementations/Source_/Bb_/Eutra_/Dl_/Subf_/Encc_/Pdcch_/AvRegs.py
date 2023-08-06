from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AvRegs:
	"""AvRegs commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("avRegs", core, parent)

	def get(self, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PDCCh:AVRegs \n
		Snippet: value: int = driver.source.bb.eutra.dl.subf.encc.pdcch.avRegs.get(stream = repcap.Stream.Default) \n
		Defines the number of the REGs that are available for the PDCCH allocation. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:return: avail_region_coun: integer Range: 0 to 1E5"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PDCCh:AVRegs?')
		return Conversions.str_to_int(response)

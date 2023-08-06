from typing import List

from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal.Types import DataType
from ..........Internal.StructBase import StructBase
from ..........Internal.ArgStruct import ArgStruct
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pattern:
	"""Pattern commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pattern", core, parent)

	# noinspection PyTypeChecker
	class PatternStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Pattern: List[str]: numeric
			- Bit_Count: int: integer Range: 1 to 64"""
		__meta_args_list = [
			ArgStruct('Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pattern: List[str] = None
			self.Bit_Count: int = None

	def set(self, structure: PatternStruct, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PDCCh:DCRegs:PATTern \n
		Snippet: driver.source.bb.eutra.dl.subf.encc.pdcch.dcRegs.pattern.set(value = [PROPERTY_STRUCT_NAME](), stream = repcap.Stream.Default) \n
		Selects the bit pattern for the PATT selection. \n
			:param structure: for set value, see the help for PatternStruct structure arguments.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PDCCh:DCRegs:PATTern', structure)

	def get(self, stream=repcap.Stream.Default) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PDCCh:DCRegs:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.eutra.dl.subf.encc.pdcch.dcRegs.pattern.get(stream = repcap.Stream.Default) \n
		Selects the bit pattern for the PATT selection. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:return: structure: for return value, see the help for PatternStruct structure arguments."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PDCCh:DCRegs:PATTern?', self.__class__.PatternStruct())

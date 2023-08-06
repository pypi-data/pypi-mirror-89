from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.Types import DataType
from .........Internal.StructBase import StructBase
from .........Internal.ArgStruct import ArgStruct
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pattern:
	"""Pattern commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pattern", core, parent)

	# noinspection PyTypeChecker
	class PatternStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Pattern: List[str]: 64 bits
			- Bit_Count: int: integer Range: 1 to 64"""
		__meta_args_list = [
			ArgStruct('Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pattern: List[str] = None
			self.Bit_Count: int = None

	def set(self, structure: PatternStruct, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:SSPBch<ST>:CCODing:PATTern \n
		Snippet: driver.source.bb.nr5G.node.cell.sspbch.ccoding.pattern.set(value = [PROPERTY_STRUCT_NAME](), channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets a bit pattern as a data source. \n
			:param structure: for set value, see the help for PatternStruct structure arguments.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sspbch')"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:SSPBch{stream_cmd_val}:CCODing:PATTern', structure)

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:SSPBch<ST>:CCODing:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.nr5G.node.cell.sspbch.ccoding.pattern.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets a bit pattern as a data source. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sspbch')
			:return: structure: for return value, see the help for PatternStruct structure arguments."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:SSPBch{stream_cmd_val}:CCODing:PATTern?', self.__class__.PatternStruct())

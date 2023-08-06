from typing import List

from ..............Internal.Core import Core
from ..............Internal.CommandsGroup import CommandsGroup
from ..............Internal.Types import DataType
from ..............Internal.StructBase import StructBase
from ..............Internal.ArgStruct import ArgStruct
from .............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pattern:
	"""Pattern commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pattern", core, parent)

	# noinspection PyTypeChecker
	class PatternStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Aack_Pattern: List[str]: 128 bits Bit pattern
			- Bitcount: int: integer Pattern length, should be the same as the length set with the command [CMDLINK: BB:NR5G:SCHed:CELLch0:SUBFst0:USERdir0:BWPartgr0:ALLocuser0:PUCCh:PL:ACK:BITS CMDLINK]. Range: 1 to 128"""
		__meta_args_list = [
			ArgStruct('Aack_Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Aack_Pattern: List[str] = None
			self.Bitcount: int = None

	def set(self, structure: PatternStruct, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:PUCCh:PL:ACK:PATTern \n
		Snippet: driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.pucch.pl.ack.pattern.set(value = [PROPERTY_STRUCT_NAME](), channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the ACK/UCI bits in pattern form. \n
			:param structure: for set value, see the help for PatternStruct structure arguments.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:PUCCh:PL:ACK:PATTern', structure)

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:PUCCh:PL:ACK:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.pucch.pl.ack.pattern.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the ACK/UCI bits in pattern form. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:return: structure: for return value, see the help for PatternStruct structure arguments."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:PUCCh:PL:ACK:PATTern?', self.__class__.PatternStruct())

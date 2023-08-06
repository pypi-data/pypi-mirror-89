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
			- Ack_Pattern: List[str]: 128 bits Bit pattern
			- Ack_Bitcount: int: integer Pattern length, should be the same as the length set with the command [CMDLINK: BB:NR5G:SCHed:CELLch0:SUBFst0:USERdir0:BWPartgr0:ALLocuser0:PUSCh:UCI:ACK:BITS CMDLINK]. Range: 0 to 128"""
		__meta_args_list = [
			ArgStruct('Ack_Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Ack_Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ack_Pattern: List[str] = None
			self.Ack_Bitcount: int = None

	def set(self, structure: PatternStruct, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:PUSCh:UCI:ACK:PATTern \n
		Snippet: driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.pusch.uci.ack.pattern.set(value = [PROPERTY_STRUCT_NAME](), channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the ACK/CSI 1/CSI 2 bits in pattern form. \n
			:param structure: for set value, see the help for PatternStruct structure arguments.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:PUSCh:UCI:ACK:PATTern', structure)

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:PUSCh:UCI:ACK:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.pusch.uci.ack.pattern.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the ACK/CSI 1/CSI 2 bits in pattern form. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:return: structure: for return value, see the help for PatternStruct structure arguments."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:PUSCh:UCI:ACK:PATTern?', self.__class__.PatternStruct())

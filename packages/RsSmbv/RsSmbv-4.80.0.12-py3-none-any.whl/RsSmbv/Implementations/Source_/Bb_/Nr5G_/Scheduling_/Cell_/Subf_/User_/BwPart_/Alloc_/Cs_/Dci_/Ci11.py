from typing import List

from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal.Types import DataType
from .............Internal.StructBase import StructBase
from .............Internal.ArgStruct import ArgStruct
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ci11:
	"""Ci11 commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ci11", core, parent)

	# noinspection PyTypeChecker
	class Ci11Struct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Pattern: List[str]: 7 bits Bit pattern for the cancellation indication.
			- Bit_Count: int: integer Range: 1 to 7"""
		__meta_args_list = [
			ArgStruct('Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pattern: List[str] = None
			self.Bit_Count: int = None

	def set(self, structure: Ci11Struct, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:CS:DCI:CI11 \n
		Snippet: driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.cs.dci.ci11.set(value = [PROPERTY_STRUCT_NAME](), channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the cancellation indication parameters for the DCI format 2_4. \n
			:param structure: for set value, see the help for Ci11Struct structure arguments.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:CS:DCI:CI11', structure)

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> Ci11Struct:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:CS:DCI:CI11 \n
		Snippet: value: Ci11Struct = driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.cs.dci.ci11.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the cancellation indication parameters for the DCI format 2_4. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:return: structure: for return value, see the help for Ci11Struct structure arguments."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:CS:DCI:CI11?', self.__class__.Ci11Struct())

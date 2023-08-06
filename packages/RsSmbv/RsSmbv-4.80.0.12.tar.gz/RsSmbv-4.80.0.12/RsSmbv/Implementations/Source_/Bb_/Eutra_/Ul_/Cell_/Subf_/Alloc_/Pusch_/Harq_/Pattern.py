from typing import List

from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal.Types import DataType
from ...........Internal.StructBase import StructBase
from ...........Internal.ArgStruct import ArgStruct
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pattern:
	"""Pattern commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pattern", core, parent)

	# noinspection PyTypeChecker
	class PatternStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Pattern: List[str]: 1024 bits
			- Bit_Count: List[str]: 1024 bits Range: 1 to 64"""
		__meta_args_list = [
			ArgStruct('Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct('Bit_Count', DataType.RawStringList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pattern: List[str] = None
			self.Bit_Count: List[str] = None

	def set(self, structure: PatternStruct, carrierComponent=repcap.CarrierComponent.Default, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:[CELL<CCIDX>]:[SUBF<ST>]:ALLoc<CH>:PUSCh:HARQ:PATTern \n
		Snippet: driver.source.bb.eutra.ul.cell.subf.alloc.pusch.harq.pattern.set(value = [PROPERTY_STRUCT_NAME](), carrierComponent = repcap.CarrierComponent.Default, stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the ACK/NACK pattern for the PUSCH. \n
			:param structure: for set value, see the help for PatternStruct structure arguments.
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')"""
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:EUTRa:UL:CELL{carrierComponent_cmd_val}:SUBF{stream_cmd_val}:ALLoc{channel_cmd_val}:PUSCh:HARQ:PATTern', structure)

	def get(self, carrierComponent=repcap.CarrierComponent.Default, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:[CELL<CCIDX>]:[SUBF<ST>]:ALLoc<CH>:PUSCh:HARQ:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.eutra.ul.cell.subf.alloc.pusch.harq.pattern.get(carrierComponent = repcap.CarrierComponent.Default, stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the ACK/NACK pattern for the PUSCH. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: structure: for return value, see the help for PatternStruct structure arguments."""
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:EUTRa:UL:CELL{carrierComponent_cmd_val}:SUBF{stream_cmd_val}:ALLoc{channel_cmd_val}:PUSCh:HARQ:PATTern?', self.__class__.PatternStruct())

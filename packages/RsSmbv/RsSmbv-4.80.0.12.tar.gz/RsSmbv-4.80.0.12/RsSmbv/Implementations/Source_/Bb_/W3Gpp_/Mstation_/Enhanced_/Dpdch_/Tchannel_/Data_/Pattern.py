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

	def set(self, structure: PatternStruct, transportChannel=repcap.TransportChannel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation:ENHanced:DPDCh:TCHannel<DI>:DATA:PATTern \n
		Snippet: driver.source.bb.w3Gpp.mstation.enhanced.dpdch.tchannel.data.pattern.set(value = [PROPERTY_STRUCT_NAME](), transportChannel = repcap.TransportChannel.Default) \n
		The command determines the bit pattern for the PATTern data source selection for transport channels. \n
			:param structure: for set value, see the help for PatternStruct structure arguments.
			:param transportChannel: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tchannel')"""
		transportChannel_cmd_val = self._base.get_repcap_cmd_value(transportChannel, repcap.TransportChannel)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:TCHannel{transportChannel_cmd_val}:DATA:PATTern', structure)

	def get(self, transportChannel=repcap.TransportChannel.Default) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation:ENHanced:DPDCh:TCHannel<DI>:DATA:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.w3Gpp.mstation.enhanced.dpdch.tchannel.data.pattern.get(transportChannel = repcap.TransportChannel.Default) \n
		The command determines the bit pattern for the PATTern data source selection for transport channels. \n
			:param transportChannel: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tchannel')
			:return: structure: for return value, see the help for PatternStruct structure arguments."""
		transportChannel_cmd_val = self._base.get_repcap_cmd_value(transportChannel, repcap.TransportChannel)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:TCHannel{transportChannel_cmd_val}:DATA:PATTern?', self.__class__.PatternStruct())

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CrcSize:
	"""CrcSize commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("crcSize", core, parent)

	def set(self, crc_size: enums.TchCrc, transportChannel=repcap.TransportChannel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation:ENHanced:DPDCh:TCHannel<DI>:CRCSize \n
		Snippet: driver.source.bb.w3Gpp.mstation.enhanced.dpdch.tchannel.crcSize.set(crc_size = enums.TchCrc._12, transportChannel = repcap.TransportChannel.Default) \n
		The command defines the CRC length for the selected transport channel. It is also possible to deactivate checksum
		determination. \n
			:param crc_size: NONE| 8| 12| 16| 24
			:param transportChannel: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tchannel')"""
		param = Conversions.enum_scalar_to_str(crc_size, enums.TchCrc)
		transportChannel_cmd_val = self._base.get_repcap_cmd_value(transportChannel, repcap.TransportChannel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:TCHannel{transportChannel_cmd_val}:CRCSize {param}')

	# noinspection PyTypeChecker
	def get(self, transportChannel=repcap.TransportChannel.Default) -> enums.TchCrc:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation:ENHanced:DPDCh:TCHannel<DI>:CRCSize \n
		Snippet: value: enums.TchCrc = driver.source.bb.w3Gpp.mstation.enhanced.dpdch.tchannel.crcSize.get(transportChannel = repcap.TransportChannel.Default) \n
		The command defines the CRC length for the selected transport channel. It is also possible to deactivate checksum
		determination. \n
			:param transportChannel: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tchannel')
			:return: crc_size: NONE| 8| 12| 16| 24"""
		transportChannel_cmd_val = self._base.get_repcap_cmd_value(transportChannel, repcap.TransportChannel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:TCHannel{transportChannel_cmd_val}:CRCSize?')
		return Conversions.str_to_scalar_enum(response, enums.TchCrc)

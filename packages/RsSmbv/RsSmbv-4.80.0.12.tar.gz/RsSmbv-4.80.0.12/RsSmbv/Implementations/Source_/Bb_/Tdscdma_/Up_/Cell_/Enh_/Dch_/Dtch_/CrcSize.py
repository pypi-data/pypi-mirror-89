from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import enums
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CrcSize:
	"""CrcSize commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("crcSize", core, parent)

	def set(self, crc_size: enums.TchCrc, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:UP:CELL<ST>:ENH:DCH:DTCH<CH>:CRCSize \n
		Snippet: driver.source.bb.tdscdma.up.cell.enh.dch.dtch.crcSize.set(crc_size = enums.TchCrc._12, stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the type (length) of the CRC. \n
			:param crc_size: NONE| 8| 12| 16| 24
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dtch')"""
		param = Conversions.enum_scalar_to_str(crc_size, enums.TchCrc)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:UP:CELL{stream_cmd_val}:ENH:DCH:DTCH{channel_cmd_val}:CRCSize {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> enums.TchCrc:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:UP:CELL<ST>:ENH:DCH:DTCH<CH>:CRCSize \n
		Snippet: value: enums.TchCrc = driver.source.bb.tdscdma.up.cell.enh.dch.dtch.crcSize.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the type (length) of the CRC. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dtch')
			:return: crc_size: NONE| 8| 12| 16| 24"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:UP:CELL{stream_cmd_val}:ENH:DCH:DTCH{channel_cmd_val}:CRCSize?')
		return Conversions.str_to_scalar_enum(response, enums.TchCrc)

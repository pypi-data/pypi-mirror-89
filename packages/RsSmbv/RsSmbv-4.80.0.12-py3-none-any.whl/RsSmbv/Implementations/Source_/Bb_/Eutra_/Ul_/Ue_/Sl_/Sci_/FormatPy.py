from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FormatPy:
	"""FormatPy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("formatPy", core, parent)

	def set(self, sci_format: enums.EutraSciFormat, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:SCI<CH>:FORMat \n
		Snippet: driver.source.bb.eutra.ul.ue.sl.sci.formatPy.set(sci_format = enums.EutraSciFormat._0, stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Queries the SCI (SL control information) format. \n
			:param sci_format: 0
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sci')"""
		param = Conversions.enum_scalar_to_str(sci_format, enums.EutraSciFormat)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:SL:SCI{channel_cmd_val}:FORMat {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> enums.EutraSciFormat:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:SCI<CH>:FORMat \n
		Snippet: value: enums.EutraSciFormat = driver.source.bb.eutra.ul.ue.sl.sci.formatPy.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Queries the SCI (SL control information) format. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sci')
			:return: sci_format: 0"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:SL:SCI{channel_cmd_val}:FORMat?')
		return Conversions.str_to_scalar_enum(response, enums.EutraSciFormat)

from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import enums
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FormatPy:
	"""FormatPy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("formatPy", core, parent)

	def set(self, format_py: enums.PositionFormat, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:FDB<ST>:DDLocation:COORdinates:FORMat \n
		Snippet: driver.source.bb.gbas.vdb.mconfig.fdb.ddlocation.coordinates.formatPy.set(format_py = enums.PositionFormat.DECimal, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the format in which the latitude and longitude are set. \n
			:param format_py: DMS| DECimal
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fdb')"""
		param = Conversions.enum_scalar_to_str(format_py, enums.PositionFormat)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:FDB{stream_cmd_val}:DDLocation:COORdinates:FORMat {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.PositionFormat:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:FDB<ST>:DDLocation:COORdinates:FORMat \n
		Snippet: value: enums.PositionFormat = driver.source.bb.gbas.vdb.mconfig.fdb.ddlocation.coordinates.formatPy.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the format in which the latitude and longitude are set. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fdb')
			:return: format_py: DMS| DECimal"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:FDB{stream_cmd_val}:DDLocation:COORdinates:FORMat?')
		return Conversions.str_to_scalar_enum(response, enums.PositionFormat)

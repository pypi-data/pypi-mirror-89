from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.StructBase import StructBase
from .........Internal.ArgStruct import ArgStruct
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Time:
	"""Time commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("time", core, parent)

	# noinspection PyTypeChecker
	class TimeStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Hour: int: integer Range: 0 to 23
			- Minute: int: integer Range: 0 to 59
			- Second: float: float Range: 0 to 59.999"""
		__meta_args_list = [
			ArgStruct.scalar_int('Hour'),
			ArgStruct.scalar_int('Minute'),
			ArgStruct.scalar_float('Second')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Hour: int = None
			self.Minute: int = None
			self.Second: float = None

	def set(self, structure: TimeStruct, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:SBAS<ST>:SIMulated:ORBit:TIME \n
		Snippet: driver.source.bb.gnss.svid.sbas.simulated.orbit.time.set(value = [PROPERTY_STRUCT_NAME](), channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the reference time. \n
			:param structure: for set value, see the help for TimeStruct structure arguments.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbas')"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:SBAS{stream_cmd_val}:SIMulated:ORBit:TIME', structure)

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> TimeStruct:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:SBAS<ST>:SIMulated:ORBit:TIME \n
		Snippet: value: TimeStruct = driver.source.bb.gnss.svid.sbas.simulated.orbit.time.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the reference time. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbas')
			:return: structure: for return value, see the help for TimeStruct structure arguments."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:SBAS{stream_cmd_val}:SIMulated:ORBit:TIME?', self.__class__.TimeStruct())

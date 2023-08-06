from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal.StructBase import StructBase
from ..........Internal.ArgStruct import ArgStruct
from ..........Internal.RepeatedCapability import RepeatedCapability
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Wgs:
	"""Wgs commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("wgs", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def repcap_channel_set(self, enum_value: repcap.Channel) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Channel.Default
		Default value after init: Channel.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_channel_get(self) -> repcap.Channel:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	# noinspection PyTypeChecker
	class WgsStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Longitude: float: float Range: -180 to 180
			- Latitude: float: float Range: -90 to 90
			- Altitude: float: float Range: -10E3 to 50E6"""
		__meta_args_list = [
			ArgStruct.scalar_float('Longitude'),
			ArgStruct.scalar_float('Latitude'),
			ArgStruct.scalar_float('Altitude')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Longitude: float = None
			self.Latitude: float = None
			self.Altitude: float = None

	def set(self, structure: WgsStruct, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GLONass<ST>:LOCation:COORdinates:DECimal:[WGS<CH>] \n
		Snippet: driver.source.bb.gnss.adGeneration.glonass.location.coordinates.decimal.wgs.set(value = [PROPERTY_STRUCT_NAME](), stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the geographic reference location in decimal format. \n
			:param structure: for set value, see the help for WgsStruct structure arguments.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Glonass')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Wgs')"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:GLONass{stream_cmd_val}:LOCation:COORdinates:DECimal:WGS{channel_cmd_val}', structure)

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> WgsStruct:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GLONass<ST>:LOCation:COORdinates:DECimal:[WGS<CH>] \n
		Snippet: value: WgsStruct = driver.source.bb.gnss.adGeneration.glonass.location.coordinates.decimal.wgs.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the geographic reference location in decimal format. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Glonass')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Wgs')
			:return: structure: for return value, see the help for WgsStruct structure arguments."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:GLONass{stream_cmd_val}:LOCation:COORdinates:DECimal:WGS{channel_cmd_val}?', self.__class__.WgsStruct())

	def clone(self) -> 'Wgs':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Wgs(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

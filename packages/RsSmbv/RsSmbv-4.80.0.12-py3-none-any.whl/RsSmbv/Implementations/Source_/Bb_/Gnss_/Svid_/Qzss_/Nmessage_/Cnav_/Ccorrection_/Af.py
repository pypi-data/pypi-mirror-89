from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from ..........Internal.RepeatedCapability import RepeatedCapability
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Af:
	"""Af commands group definition. 2 total commands, 1 Sub-groups, 1 group commands
	Repeated Capability: GnssIndex, default value after init: GnssIndex.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("af", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_gnssIndex_get', 'repcap_gnssIndex_set', repcap.GnssIndex.Nr0)

	def repcap_gnssIndex_set(self, enum_value: repcap.GnssIndex) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to GnssIndex.Default
		Default value after init: GnssIndex.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_gnssIndex_get(self) -> repcap.GnssIndex:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def unscaled(self):
		"""unscaled commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_unscaled'):
			from .Af_.Unscaled import Unscaled
			self._unscaled = Unscaled(self._core, self._base)
		return self._unscaled

	def set(self, af: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default, gnssIndex=repcap.GnssIndex.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:QZSS<ST>:NMESsage:CNAV:CCORrection:AF<S2US> \n
		Snippet: driver.source.bb.gnss.svid.qzss.nmessage.cnav.ccorrection.af.set(af = 1, channel = repcap.Channel.Default, stream = repcap.Stream.Default, gnssIndex = repcap.GnssIndex.Default) \n
		Sets the parameter AF 0 to 2. \n
			:param af: integer
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qzss')
			:param gnssIndex: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Af')"""
		param = Conversions.decimal_value_to_str(af)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		gnssIndex_cmd_val = self._base.get_repcap_cmd_value(gnssIndex, repcap.GnssIndex)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:QZSS{stream_cmd_val}:NMESsage:CNAV:CCORrection:AF{gnssIndex_cmd_val} {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, gnssIndex=repcap.GnssIndex.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:QZSS<ST>:NMESsage:CNAV:CCORrection:AF<S2US> \n
		Snippet: value: int = driver.source.bb.gnss.svid.qzss.nmessage.cnav.ccorrection.af.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default, gnssIndex = repcap.GnssIndex.Default) \n
		Sets the parameter AF 0 to 2. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qzss')
			:param gnssIndex: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Af')
			:return: af: integer"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		gnssIndex_cmd_val = self._base.get_repcap_cmd_value(gnssIndex, repcap.GnssIndex)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:QZSS{stream_cmd_val}:NMESsage:CNAV:CCORrection:AF{gnssIndex_cmd_val}?')
		return Conversions.str_to_int(response)

	def clone(self) -> 'Af':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Af(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

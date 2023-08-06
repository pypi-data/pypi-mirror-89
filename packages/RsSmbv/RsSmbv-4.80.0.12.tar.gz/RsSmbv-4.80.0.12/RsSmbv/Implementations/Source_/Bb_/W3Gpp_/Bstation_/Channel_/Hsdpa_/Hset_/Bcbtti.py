from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bcbtti:
	"""Bcbtti commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: TwoStreams, default value after init: TwoStreams.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bcbtti", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_twoStreams_get', 'repcap_twoStreams_set', repcap.TwoStreams.Nr0)

	def repcap_twoStreams_set(self, enum_value: repcap.TwoStreams) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to TwoStreams.Default
		Default value after init: TwoStreams.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_twoStreams_get(self) -> repcap.TwoStreams:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default, twoStreams=repcap.TwoStreams.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:HSDPa:HSET:BCBTti<DI> \n
		Snippet: value: float = driver.source.bb.w3Gpp.bstation.channel.hsdpa.hset.bcbtti.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default, twoStreams = repcap.TwoStreams.Default) \n
		Displays the binary channel bits per TTI and per stream.
			INTRO_CMD_HELP: The value displayed is calculated upon the values sets with the commands: \n
			- BB:W3GPp:BSTation<st>:CHANnel<ch0>:HSDPa:HSET:MODulation<di>,
			- method RsSmbv.Source.Bb.W3Gpp.Bstation.Channel.SymbolRate.set and
			- method RsSmbv.Source.Bb.W3Gpp.Bstation.Channel.Hsdpa.Hset.HscCode.set. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:param twoStreams: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bcbtti')
			:return: bcbtti: float"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		twoStreams_cmd_val = self._base.get_repcap_cmd_value(twoStreams, repcap.TwoStreams)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:HSDPa:HSET:BCBTti{twoStreams_cmd_val}?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'Bcbtti':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Bcbtti(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

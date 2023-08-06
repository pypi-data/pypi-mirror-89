from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Atwo:
	"""Atwo commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("atwo", core, parent)

	@property
	def unscaled(self):
		"""unscaled commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_unscaled'):
			from .Atwo_.Unscaled import Unscaled
			self._unscaled = Unscaled(self._core, self._base)
		return self._unscaled

	def set(self, a_2: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SV:QZSS<ST>:NMESsage:CNAV:TIME:CONVersion:UTC<CH>:ATWO \n
		Snippet: driver.source.bb.gnss.sv.qzss.nmessage.cnav.time.conversion.utc.atwo.set(a_2 = 1, stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the A2 parameter. \n
			:param a_2: integer Range: -64 to 63
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qzss')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Utc')"""
		param = Conversions.decimal_value_to_str(a_2)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SV:QZSS{stream_cmd_val}:NMESsage:CNAV:TIME:CONVersion:UTC{channel_cmd_val}:ATWO {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SV:QZSS<ST>:NMESsage:CNAV:TIME:CONVersion:UTC<CH>:ATWO \n
		Snippet: value: int = driver.source.bb.gnss.sv.qzss.nmessage.cnav.time.conversion.utc.atwo.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the A2 parameter. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qzss')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Utc')
			:return: a_2: integer Range: -64 to 63"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SV:QZSS{stream_cmd_val}:NMESsage:CNAV:TIME:CONVersion:UTC{channel_cmd_val}:ATWO?')
		return Conversions.str_to_int(response)

	def clone(self) -> 'Atwo':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Atwo(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

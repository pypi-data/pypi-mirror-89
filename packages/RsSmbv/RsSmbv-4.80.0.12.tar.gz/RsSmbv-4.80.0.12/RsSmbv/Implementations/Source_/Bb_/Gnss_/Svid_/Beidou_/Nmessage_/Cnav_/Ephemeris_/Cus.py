from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cus:
	"""Cus commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cus", core, parent)

	@property
	def unscaled(self):
		"""unscaled commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_unscaled'):
			from .Cus_.Unscaled import Unscaled
			self._unscaled = Unscaled(self._core, self._base)
		return self._unscaled

	def set(self, cus: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:BEIDou<ST>:NMESsage:CNAV:EPHemeris:CUS \n
		Snippet: driver.source.bb.gnss.svid.beidou.nmessage.cnav.ephemeris.cus.set(cus = 1, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the sine difference of latitude. \n
			:param cus: integer
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Beidou')"""
		param = Conversions.decimal_value_to_str(cus)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:BEIDou{stream_cmd_val}:NMESsage:CNAV:EPHemeris:CUS {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:BEIDou<ST>:NMESsage:CNAV:EPHemeris:CUS \n
		Snippet: value: int = driver.source.bb.gnss.svid.beidou.nmessage.cnav.ephemeris.cus.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the sine difference of latitude. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Beidou')
			:return: cus: integer"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:BEIDou{stream_cmd_val}:NMESsage:CNAV:EPHemeris:CUS?')
		return Conversions.str_to_int(response)

	def clone(self) -> 'Cus':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Cus(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

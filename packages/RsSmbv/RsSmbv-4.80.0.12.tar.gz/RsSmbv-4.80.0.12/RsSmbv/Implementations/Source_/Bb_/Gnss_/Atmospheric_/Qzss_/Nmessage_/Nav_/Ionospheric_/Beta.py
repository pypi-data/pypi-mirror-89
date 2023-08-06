from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from ..........Internal.RepeatedCapability import RepeatedCapability
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Beta:
	"""Beta commands group definition. 2 total commands, 1 Sub-groups, 1 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("beta", core, parent)
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

	@property
	def unscaled(self):
		"""unscaled commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_unscaled'):
			from .Beta_.Unscaled import Unscaled
			self._unscaled = Unscaled(self._core, self._base)
		return self._unscaled

	def set(self, beta: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ATMospheric:QZSS:[NMESsage]:[NAV]:IONospheric:BETA<CH> \n
		Snippet: driver.source.bb.gnss.atmospheric.qzss.nmessage.nav.ionospheric.beta.set(beta = 1, channel = repcap.Channel.Default) \n
		Sets the parameters beta_0 to beta_3 of the satellite's navigation message. \n
			:param beta: integer Range: -128 to 127
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Beta')"""
		param = Conversions.decimal_value_to_str(beta)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ATMospheric:QZSS:NMESsage:NAV:IONospheric:BETA{channel_cmd_val} {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ATMospheric:QZSS:[NMESsage]:[NAV]:IONospheric:BETA<CH> \n
		Snippet: value: int = driver.source.bb.gnss.atmospheric.qzss.nmessage.nav.ionospheric.beta.get(channel = repcap.Channel.Default) \n
		Sets the parameters beta_0 to beta_3 of the satellite's navigation message. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Beta')
			:return: beta: integer Range: -128 to 127"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:ATMospheric:QZSS:NMESsage:NAV:IONospheric:BETA{channel_cmd_val}?')
		return Conversions.str_to_int(response)

	def clone(self) -> 'Beta':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Beta(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

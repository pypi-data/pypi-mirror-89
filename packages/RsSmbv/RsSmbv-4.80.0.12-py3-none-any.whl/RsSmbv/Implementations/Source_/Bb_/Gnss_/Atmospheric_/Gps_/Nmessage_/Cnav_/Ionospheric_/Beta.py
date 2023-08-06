from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Beta:
	"""Beta commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("beta", core, parent)

	@property
	def unscaled(self):
		"""unscaled commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_unscaled'):
			from .Beta_.Unscaled import Unscaled
			self._unscaled = Unscaled(self._core, self._base)
		return self._unscaled

	def set(self, beta: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ATMospheric:GPS:[NMESsage]:[CNAV]:IONospheric:BETA<CH> \n
		Snippet: driver.source.bb.gnss.atmospheric.gps.nmessage.cnav.ionospheric.beta.set(beta = 1, channel = repcap.Channel.Default) \n
		Sets the parameters beta_0 to beta_3 of the satellite's navigation message. \n
			:param beta: integer Range: -128 to 127
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')"""
		param = Conversions.decimal_value_to_str(beta)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ATMospheric:GPS:NMESsage:CNAV:IONospheric:BETA{channel_cmd_val} {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ATMospheric:GPS:[NMESsage]:[CNAV]:IONospheric:BETA<CH> \n
		Snippet: value: int = driver.source.bb.gnss.atmospheric.gps.nmessage.cnav.ionospheric.beta.get(channel = repcap.Channel.Default) \n
		Sets the parameters beta_0 to beta_3 of the satellite's navigation message. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')
			:return: beta: integer Range: -128 to 127"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:ATMospheric:GPS:NMESsage:CNAV:IONospheric:BETA{channel_cmd_val}?')
		return Conversions.str_to_int(response)

	def clone(self) -> 'Beta':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Beta(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Unscaled:
	"""Unscaled commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("unscaled", core, parent)

	def set(self, alpha_unscaled: float, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ATMospheric:GPS:[NMESsage]:[LNAV]:IONospheric:ALPHa<CH>:UNSCaled \n
		Snippet: driver.source.bb.gnss.atmospheric.gps.nmessage.lnav.ionospheric.alpha.unscaled.set(alpha_unscaled = 1.0, channel = repcap.Channel.Default) \n
		Sets the parameters alpha_0 to alpha_3 of the satellite's navigation message. \n
			:param alpha_unscaled: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')"""
		param = Conversions.decimal_value_to_str(alpha_unscaled)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ATMospheric:GPS:NMESsage:LNAV:IONospheric:ALPHa{channel_cmd_val}:UNSCaled {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ATMospheric:GPS:[NMESsage]:[LNAV]:IONospheric:ALPHa<CH>:UNSCaled \n
		Snippet: value: float = driver.source.bb.gnss.atmospheric.gps.nmessage.lnav.ionospheric.alpha.unscaled.get(channel = repcap.Channel.Default) \n
		Sets the parameters alpha_0 to alpha_3 of the satellite's navigation message. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')
			:return: alpha_unscaled: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:ATMospheric:GPS:NMESsage:LNAV:IONospheric:ALPHa{channel_cmd_val}:UNSCaled?')
		return Conversions.str_to_float(response)

from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sf:
	"""Sf commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sf", core, parent)

	def set(self, sf: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ATMospheric:GALileo:[NMESsage]:[FNAV]:IONospheric:SF<CH> \n
		Snippet: driver.source.bb.gnss.atmospheric.galileo.nmessage.fnav.ionospheric.sf.set(sf = 1, channel = repcap.Channel.Default) \n
		Sets the parameters ionospheric disturbance flag for region 1 to 5 of the satellite's navigation message. \n
			:param sf: integer Range: 0 to 1
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Galileo')"""
		param = Conversions.decimal_value_to_str(sf)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ATMospheric:GALileo:NMESsage:FNAV:IONospheric:SF{channel_cmd_val} {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ATMospheric:GALileo:[NMESsage]:[FNAV]:IONospheric:SF<CH> \n
		Snippet: value: int = driver.source.bb.gnss.atmospheric.galileo.nmessage.fnav.ionospheric.sf.get(channel = repcap.Channel.Default) \n
		Sets the parameters ionospheric disturbance flag for region 1 to 5 of the satellite's navigation message. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Galileo')
			:return: sf: integer Range: 0 to 1"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:ATMospheric:GALileo:NMESsage:FNAV:IONospheric:SF{channel_cmd_val}?')
		return Conversions.str_to_int(response)

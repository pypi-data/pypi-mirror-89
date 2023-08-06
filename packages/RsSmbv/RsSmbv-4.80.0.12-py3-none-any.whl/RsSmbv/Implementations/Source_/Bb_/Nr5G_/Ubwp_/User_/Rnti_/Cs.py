from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cs:
	"""Cs commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cs", core, parent)

	def set(self, cs_rnti: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:RNTI:CS \n
		Snippet: driver.source.bb.nr5G.ubwp.user.rnti.cs.set(cs_rnti = 1, channel = repcap.Channel.Default) \n
		Sets the CS-RNTI of the user. It is a unique UE identification used for semi-persistent scheduling in the downlink. \n
			:param cs_rnti: integer Range: 1 to 65519
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.decimal_value_to_str(cs_rnti)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:RNTI:CS {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:RNTI:CS \n
		Snippet: value: int = driver.source.bb.nr5G.ubwp.user.rnti.cs.get(channel = repcap.Channel.Default) \n
		Sets the CS-RNTI of the user. It is a unique UE identification used for semi-persistent scheduling in the downlink. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: cs_rnti: integer Range: 1 to 65519"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:RNTI:CS?')
		return Conversions.str_to_int(response)

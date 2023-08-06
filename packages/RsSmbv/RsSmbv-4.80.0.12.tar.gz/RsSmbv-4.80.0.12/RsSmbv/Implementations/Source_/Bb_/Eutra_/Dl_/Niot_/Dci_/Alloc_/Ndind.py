from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ndind:
	"""Ndind commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ndind", core, parent)

	def set(self, new_data_ind: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:NIOT:DCI:ALLoc<CH>:NDINd \n
		Snippet: driver.source.bb.eutra.dl.niot.dci.alloc.ndind.set(new_data_ind = False, channel = repcap.Channel.Default) \n
		Sets the DCI field new data indicator. \n
			:param new_data_ind: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')"""
		param = Conversions.bool_to_str(new_data_ind)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:DCI:ALLoc{channel_cmd_val}:NDINd {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:NIOT:DCI:ALLoc<CH>:NDINd \n
		Snippet: value: bool = driver.source.bb.eutra.dl.niot.dci.alloc.ndind.get(channel = repcap.Channel.Default) \n
		Sets the DCI field new data indicator. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: new_data_ind: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:DCI:ALLoc{channel_cmd_val}:NDINd?')
		return Conversions.str_to_bool(response)

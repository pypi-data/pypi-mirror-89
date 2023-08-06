from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Snumber:
	"""Snumber commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("snumber", core, parent)

	def set(self, starting_number: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:NIOT:DCI:ALLoc<CH>:NPRach:SNUMber \n
		Snippet: driver.source.bb.eutra.dl.niot.dci.alloc.nprach.snumber.set(starting_number = 1, channel = repcap.Channel.Default) \n
		Sets the DCI field starting number of NPRACH repetitions (IRep) . \n
			:param starting_number: integer Range: 0 to 2
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')"""
		param = Conversions.decimal_value_to_str(starting_number)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:DCI:ALLoc{channel_cmd_val}:NPRach:SNUMber {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:NIOT:DCI:ALLoc<CH>:NPRach:SNUMber \n
		Snippet: value: int = driver.source.bb.eutra.dl.niot.dci.alloc.nprach.snumber.get(channel = repcap.Channel.Default) \n
		Sets the DCI field starting number of NPRACH repetitions (IRep) . \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: starting_number: integer Range: 0 to 2"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:DCI:ALLoc{channel_cmd_val}:NPRach:SNUMber?')
		return Conversions.str_to_int(response)

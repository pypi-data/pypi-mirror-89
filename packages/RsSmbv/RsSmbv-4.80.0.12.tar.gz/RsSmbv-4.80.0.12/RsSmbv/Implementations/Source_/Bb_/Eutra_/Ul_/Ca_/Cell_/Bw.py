from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bw:
	"""Bw commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bw", core, parent)

	def set(self, ulca_bw: enums.EutraCaChannelBandwidth, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:CA:CELL<CH>:BW \n
		Snippet: driver.source.bb.eutra.ul.ca.cell.bw.set(ulca_bw = enums.EutraCaChannelBandwidth.BW1_40, channel = repcap.Channel.Default) \n
		Sets the bandwidth of the corresponding component carrier. \n
			:param ulca_bw: BW1_40| BW3_00| BW5_00| BW10_00| BW15_00| BW20_00
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.enum_scalar_to_str(ulca_bw, enums.EutraCaChannelBandwidth)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:CA:CELL{channel_cmd_val}:BW {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EutraCaChannelBandwidth:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:CA:CELL<CH>:BW \n
		Snippet: value: enums.EutraCaChannelBandwidth = driver.source.bb.eutra.ul.ca.cell.bw.get(channel = repcap.Channel.Default) \n
		Sets the bandwidth of the corresponding component carrier. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: ulca_bw: BW1_40| BW3_00| BW5_00| BW10_00| BW15_00| BW20_00"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:CA:CELL{channel_cmd_val}:BW?')
		return Conversions.str_to_scalar_enum(response, enums.EutraCaChannelBandwidth)

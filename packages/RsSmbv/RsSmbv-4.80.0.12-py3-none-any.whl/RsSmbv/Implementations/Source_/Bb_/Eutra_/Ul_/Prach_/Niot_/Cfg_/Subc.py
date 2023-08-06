from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Subc:
	"""Subc commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("subc", core, parent)

	def set(self, subcarriers: enums.EutraPracNbiotSubcarriers, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:PRACh:NIOT:CFG<CH>:SUBC \n
		Snippet: driver.source.bb.eutra.ul.prach.niot.cfg.subc.set(subcarriers = enums.EutraPracNbiotSubcarriers._12, channel = repcap.Channel.Default) \n
		Sets the number of NPRACH subcarriers. \n
			:param subcarriers: 12| 24| 36| 48
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cfg')"""
		param = Conversions.enum_scalar_to_str(subcarriers, enums.EutraPracNbiotSubcarriers)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:PRACh:NIOT:CFG{channel_cmd_val}:SUBC {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EutraPracNbiotSubcarriers:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:PRACh:NIOT:CFG<CH>:SUBC \n
		Snippet: value: enums.EutraPracNbiotSubcarriers = driver.source.bb.eutra.ul.prach.niot.cfg.subc.get(channel = repcap.Channel.Default) \n
		Sets the number of NPRACH subcarriers. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cfg')
			:return: subcarriers: 12| 24| 36| 48"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:PRACh:NIOT:CFG{channel_cmd_val}:SUBC?')
		return Conversions.str_to_scalar_enum(response, enums.EutraPracNbiotSubcarriers)

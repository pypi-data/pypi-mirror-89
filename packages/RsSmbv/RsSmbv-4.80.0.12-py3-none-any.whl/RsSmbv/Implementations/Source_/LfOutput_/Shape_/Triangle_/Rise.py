from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rise:
	"""Rise commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rise", core, parent)

	def set(self, rise: float, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:LFOutput<CH>:SHAPe:TRIangle:RISE \n
		Snippet: driver.source.lfOutput.shape.triangle.rise.set(rise = 1.0, channel = repcap.Channel.Default) \n
		Selects the rise time for the triangle single of the LF generator. \n
			:param rise: float Range: 1E-6 to 100
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'LfOutput')"""
		param = Conversions.decimal_value_to_str(rise)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:LFOutput{channel_cmd_val}:SHAPe:TRIangle:RISE {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SCPI: [SOURce<HW>]:LFOutput<CH>:SHAPe:TRIangle:RISE \n
		Snippet: value: float = driver.source.lfOutput.shape.triangle.rise.get(channel = repcap.Channel.Default) \n
		Selects the rise time for the triangle single of the LF generator. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'LfOutput')
			:return: rise: float Range: 1E-6 to 100"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:LFOutput{channel_cmd_val}:SHAPe:TRIangle:RISE?')
		return Conversions.str_to_float(response)

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tgpl:
	"""Tgpl commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tgpl", core, parent)

	def set(self, tgpl: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation<ST>:CMODe:PATTern<CH>:TGPL \n
		Snippet: driver.source.bb.w3Gpp.bstation.cmode.pattern.tgpl.set(tgpl = 1, stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		The command sets the transmission gap pattern lengths. Setting 0 is available only for pattern 2. The transmission gap
		pattern length of the user equipment with the same suffix as the selected base station is set to the same value. \n
			:param tgpl: integer Range: 0 to 100
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Pattern')"""
		param = Conversions.decimal_value_to_str(tgpl)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CMODe:PATTern{channel_cmd_val}:TGPL {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation<ST>:CMODe:PATTern<CH>:TGPL \n
		Snippet: value: int = driver.source.bb.w3Gpp.bstation.cmode.pattern.tgpl.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		The command sets the transmission gap pattern lengths. Setting 0 is available only for pattern 2. The transmission gap
		pattern length of the user equipment with the same suffix as the selected base station is set to the same value. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Pattern')
			:return: tgpl: integer Range: 0 to 100"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CMODe:PATTern{channel_cmd_val}:TGPL?')
		return Conversions.str_to_int(response)

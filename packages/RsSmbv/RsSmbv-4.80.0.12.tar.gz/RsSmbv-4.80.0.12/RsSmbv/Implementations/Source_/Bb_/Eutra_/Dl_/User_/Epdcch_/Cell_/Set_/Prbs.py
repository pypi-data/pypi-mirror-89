from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import enums
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Prbs:
	"""Prbs commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("prbs", core, parent)

	def set(self, num_prbs: enums.EutraNumPrbs, channel=repcap.Channel.Default, stream=repcap.Stream.Default, direction=repcap.Direction.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:USER<CH>:EPDCch:CELL<ST>:SET<DIR>:PRBS \n
		Snippet: driver.source.bb.eutra.dl.user.epdcch.cell.set.prbs.set(num_prbs = enums.EutraNumPrbs.PRB2, channel = repcap.Channel.Default, stream = repcap.Stream.Default, direction = repcap.Direction.Default) \n
		Sets the number of used physical resource block (PRB) pairs. \n
			:param num_prbs: PRB2| PRB4| PRB8
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param direction: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Set')"""
		param = Conversions.enum_scalar_to_str(num_prbs, enums.EutraNumPrbs)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		direction_cmd_val = self._base.get_repcap_cmd_value(direction, repcap.Direction)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:EPDCch:CELL{stream_cmd_val}:SET{direction_cmd_val}:PRBS {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, direction=repcap.Direction.Default) -> enums.EutraNumPrbs:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:USER<CH>:EPDCch:CELL<ST>:SET<DIR>:PRBS \n
		Snippet: value: enums.EutraNumPrbs = driver.source.bb.eutra.dl.user.epdcch.cell.set.prbs.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default, direction = repcap.Direction.Default) \n
		Sets the number of used physical resource block (PRB) pairs. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param direction: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Set')
			:return: num_prbs: PRB2| PRB4| PRB8"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		direction_cmd_val = self._base.get_repcap_cmd_value(direction, repcap.Direction)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:EPDCch:CELL{stream_cmd_val}:SET{direction_cmd_val}:PRBS?')
		return Conversions.str_to_scalar_enum(response, enums.EutraNumPrbs)

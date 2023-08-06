from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nrb:
	"""Nrb commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nrb", core, parent)

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:TXBW:S60K<ST>:NRB \n
		Snippet: value: int = driver.source.bb.nr5G.node.cell.txbw.s60K.nrb.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Queries the number of available resource blocks (N_RB) . \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'S60K')
			:return: nrb: integer Range: 0 to 273"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:TXBW:S60K{stream_cmd_val}:NRB?')
		return Conversions.str_to_int(response)

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CsZero:
	"""CsZero commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("csZero", core, parent)

	def set(self, ssp_bch_cs_zero: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:SSPBch<ST>:MIB:CSZero \n
		Snippet: driver.source.bb.nr5G.node.cell.sspbch.mib.csZero.set(ssp_bch_cs_zero = 1, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the common control resource set (CORESET) of the initial downlink BWP. \n
			:param ssp_bch_cs_zero: integer Range: 0 to 15
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sspbch')"""
		param = Conversions.decimal_value_to_str(ssp_bch_cs_zero)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:SSPBch{stream_cmd_val}:MIB:CSZero {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:SSPBch<ST>:MIB:CSZero \n
		Snippet: value: int = driver.source.bb.nr5G.node.cell.sspbch.mib.csZero.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the common control resource set (CORESET) of the initial downlink BWP. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sspbch')
			:return: ssp_bch_cs_zero: integer Range: 0 to 15"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:SSPBch{stream_cmd_val}:MIB:CSZero?')
		return Conversions.str_to_int(response)

from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RmAttribute:
	"""RmAttribute commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rmAttribute", core, parent)

	def set(self, rm_attribute: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:UP:CELL<ST>:ENH:DCH:DCCH<CH>:RMATtribute \n
		Snippet: driver.source.bb.tdscdma.up.cell.enh.dch.dcch.rmAttribute.set(rm_attribute = 1, stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the rate matching. \n
			:param rm_attribute: integer Range: 16 to 1024
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dcch')"""
		param = Conversions.decimal_value_to_str(rm_attribute)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:UP:CELL{stream_cmd_val}:ENH:DCH:DCCH{channel_cmd_val}:RMATtribute {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:UP:CELL<ST>:ENH:DCH:DCCH<CH>:RMATtribute \n
		Snippet: value: int = driver.source.bb.tdscdma.up.cell.enh.dch.dcch.rmAttribute.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the rate matching. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dcch')
			:return: rm_attribute: integer Range: 16 to 1024"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:UP:CELL{stream_cmd_val}:ENH:DCH:DCCH{channel_cmd_val}:RMATtribute?')
		return Conversions.str_to_int(response)

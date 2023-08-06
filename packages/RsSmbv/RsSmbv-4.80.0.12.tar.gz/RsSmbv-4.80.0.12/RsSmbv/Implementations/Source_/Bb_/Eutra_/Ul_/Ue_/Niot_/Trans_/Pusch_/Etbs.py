from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import enums
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Etbs:
	"""Etbs commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("etbs", core, parent)

	def set(self, edt_tbs: enums.EutraNbiotEdtTbs, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:NIOT:TRANs<CH>:PUSCh:ETBS \n
		Snippet: driver.source.bb.eutra.ul.ue.niot.trans.pusch.etbs.set(edt_tbs = enums.EutraNbiotEdtTbs._1000, stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the maximum transport block size for early data transmission in UL. \n
			:param edt_tbs: 88| 328| 408| 504| 584| 680| 808| 936| 1000 Unit: bit
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trans')"""
		param = Conversions.enum_scalar_to_str(edt_tbs, enums.EutraNbiotEdtTbs)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:NIOT:TRANs{channel_cmd_val}:PUSCh:ETBS {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> enums.EutraNbiotEdtTbs:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:NIOT:TRANs<CH>:PUSCh:ETBS \n
		Snippet: value: enums.EutraNbiotEdtTbs = driver.source.bb.eutra.ul.ue.niot.trans.pusch.etbs.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the maximum transport block size for early data transmission in UL. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trans')
			:return: edt_tbs: 88| 328| 408| 504| 584| 680| 808| 936| 1000 Unit: bit"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:NIOT:TRANs{channel_cmd_val}:PUSCh:ETBS?')
		return Conversions.str_to_scalar_enum(response, enums.EutraNbiotEdtTbs)

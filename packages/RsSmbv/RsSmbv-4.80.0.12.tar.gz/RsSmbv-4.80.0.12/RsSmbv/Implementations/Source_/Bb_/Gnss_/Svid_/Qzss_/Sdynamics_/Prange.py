from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Prange:
	"""Prange commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("prange", core, parent)

	def set(self, pr_ange: float, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:QZSS<ST>:SDYNamics:PRANge \n
		Snippet: driver.source.bb.gnss.svid.qzss.sdynamics.prange.set(pr_ange = 1.0, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the initial pseudorange. \n
			:param pr_ange: float Range: 0 to 119900000
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qzss')"""
		param = Conversions.decimal_value_to_str(pr_ange)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:QZSS{stream_cmd_val}:SDYNamics:PRANge {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:QZSS<ST>:SDYNamics:PRANge \n
		Snippet: value: float = driver.source.bb.gnss.svid.qzss.sdynamics.prange.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the initial pseudorange. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qzss')
			:return: pr_ange: float Range: 0 to 119900000"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:QZSS{stream_cmd_val}:SDYNamics:PRANge?')
		return Conversions.str_to_float(response)

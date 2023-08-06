from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Acrl:
	"""Acrl commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("acrl", core, parent)

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:POWer:S15K<CH>:ACRL \n
		Snippet: value: float = driver.source.bb.nr5G.output.power.s15K.acrl.get(channel = repcap.Channel.Default) \n
		Queries the bandwidths/numerologies with their power levels. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: pow_per_bw_rel_lvl: float Range: -80 to 10"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:OUTPut:POWer:S15K{channel_cmd_val}:ACRL?')
		return Conversions.str_to_float(response)

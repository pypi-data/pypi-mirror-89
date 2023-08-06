from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NdlSymbols:
	"""NdlSymbols commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ndlSymbols", core, parent)

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TRIGger:OUTPut<CH>:SSC:NDLSymbols \n
		Snippet: value: int = driver.source.bb.nr5G.trigger.output.ssc.ndlSymbols.get(channel = repcap.Channel.Default) \n
		Queries the number of DL symbols in the special slot of a UL/DL pattern containing a marker. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: spec_slot_dls_ym: integer Range: 0 to 14"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:TRIGger:OUTPut{channel_cmd_val}:SSC:NDLSymbols?')
		return Conversions.str_to_int(response)

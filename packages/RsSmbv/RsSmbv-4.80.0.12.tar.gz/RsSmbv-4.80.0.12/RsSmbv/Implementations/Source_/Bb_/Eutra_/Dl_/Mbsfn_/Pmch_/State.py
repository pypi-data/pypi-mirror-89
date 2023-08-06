from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, pmch_state: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:MBSFn:PMCH<CH>:STATe \n
		Snippet: driver.source.bb.eutra.dl.mbsfn.pmch.state.set(pmch_state = False, channel = repcap.Channel.Default) \n
		Enables/disables the selected PMCH/MTCH. \n
			:param pmch_state: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Pmch')"""
		param = Conversions.bool_to_str(pmch_state)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:PMCH{channel_cmd_val}:STATe {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:MBSFn:PMCH<CH>:STATe \n
		Snippet: value: bool = driver.source.bb.eutra.dl.mbsfn.pmch.state.get(channel = repcap.Channel.Default) \n
		Enables/disables the selected PMCH/MTCH. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Pmch')
			:return: pmch_state: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:PMCH{channel_cmd_val}:STATe?')
		return Conversions.str_to_bool(response)

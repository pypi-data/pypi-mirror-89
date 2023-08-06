from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, mtsp: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MTSPhy:L1M<CH>:STATe \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.mtsphy.l1M.state.set(mtsp = False, channel = repcap.Channel.Default) \n
		Specifies the physical layers in master-to-slave (..:MTSPhy:..) or slave-to-master (..:STMPhy:..) direction. Information
		is signaled via LL_PHY_UPDATE_IND. You can enable one or more PHYs: L1M for LE uncoded 1 Msymbol/s PHY, L2M for LE
		uncoded 2 Msymbol/s PHY, and LCOD for LE coded 1 Msymbol/s PHY. \n
			:param mtsp: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'L1M')"""
		param = Conversions.bool_to_str(mtsp)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MTSPhy:L1M{channel_cmd_val}:STATe {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MTSPhy:L1M<CH>:STATe \n
		Snippet: value: bool = driver.source.bb.btooth.econfiguration.pconfiguration.mtsphy.l1M.state.get(channel = repcap.Channel.Default) \n
		Specifies the physical layers in master-to-slave (..:MTSPhy:..) or slave-to-master (..:STMPhy:..) direction. Information
		is signaled via LL_PHY_UPDATE_IND. You can enable one or more PHYs: L1M for LE uncoded 1 Msymbol/s PHY, L2M for LE
		uncoded 2 Msymbol/s PHY, and LCOD for LE coded 1 Msymbol/s PHY. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'L1M')
			:return: mtsp: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MTSPhy:L1M{channel_cmd_val}:STATe?')
		return Conversions.str_to_bool(response)

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CdState:
	"""CdState commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cdState", core, parent)

	def set(self, csi_rs_state: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:DRS:CELL<CH>:CDSTate \n
		Snippet: driver.source.bb.eutra.dl.drs.cell.cdState.set(csi_rs_state = False, channel = repcap.Channel.Default) \n
		Enables defining the CSI-RS part of the DRS. \n
			:param csi_rs_state: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.bool_to_str(csi_rs_state)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:DRS:CELL{channel_cmd_val}:CDSTate {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:DRS:CELL<CH>:CDSTate \n
		Snippet: value: bool = driver.source.bb.eutra.dl.drs.cell.cdState.get(channel = repcap.Channel.Default) \n
		Enables defining the CSI-RS part of the DRS. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: csi_rs_state: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:DRS:CELL{channel_cmd_val}:CDSTate?')
		return Conversions.str_to_bool(response)

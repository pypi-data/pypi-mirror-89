from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FdsState:
	"""FdsState commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fdsState", core, parent)

	def set(self, fdss: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:FDSState \n
		Snippet: driver.source.bb.gbas.vdb.mconfig.fdsState.set(fdss = False, channel = repcap.Channel.Default) \n
		Enables the configuration of Final Approach Segment (FAS) data set. \n
			:param fdss: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')"""
		param = Conversions.bool_to_str(fdss)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:FDSState {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:FDSState \n
		Snippet: value: bool = driver.source.bb.gbas.vdb.mconfig.fdsState.get(channel = repcap.Channel.Default) \n
		Enables the configuration of Final Approach Segment (FAS) data set. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:return: fdss: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:FDSState?')
		return Conversions.str_to_bool(response)

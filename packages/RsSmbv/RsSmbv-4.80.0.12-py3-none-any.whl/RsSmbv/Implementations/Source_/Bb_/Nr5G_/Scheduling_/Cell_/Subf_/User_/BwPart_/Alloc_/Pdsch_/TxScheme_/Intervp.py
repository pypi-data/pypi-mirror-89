from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal import Conversions
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Intervp:
	"""Intervp commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("intervp", core, parent)

	def set(self, user_alloc_pdsch_v: bool, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:PDSCh:TXSCheme:INTervp \n
		Snippet: driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.pdsch.txScheme.intervp.set(user_alloc_pdsch_v = False, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		If method RsSmbv.Source.Bb.Nr5G.Ubwp.User.Cell.Dl.Bwp.Pdsch.VpInter.set VP2|VP4, enables interleaved VRB-to-PRB mapping. \n
			:param user_alloc_pdsch_v: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		param = Conversions.bool_to_str(user_alloc_pdsch_v)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:PDSCh:TXSCheme:INTervp {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:PDSCh:TXSCheme:INTervp \n
		Snippet: value: bool = driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.pdsch.txScheme.intervp.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		If method RsSmbv.Source.Bb.Nr5G.Ubwp.User.Cell.Dl.Bwp.Pdsch.VpInter.set VP2|VP4, enables interleaved VRB-to-PRB mapping. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:return: user_alloc_pdsch_v: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:PDSCh:TXSCheme:INTervp?')
		return Conversions.str_to_bool(response)

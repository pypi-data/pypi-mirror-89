from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal import Conversions
from ............. import enums
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mod:
	"""Mod commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mod", core, parent)

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, codeword=repcap.Codeword.Default) -> enums.ModType:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:RESulting:ALLoc:[CW<S2US>]:MOD \n
		Snippet: value: enums.ModType = driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.resulting.alloc.cw.mod.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default, codeword = repcap.Codeword.Default) \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param codeword: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cw')
			:return: rep_user_alloc_mod: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		codeword_cmd_val = self._base.get_repcap_cmd_value(codeword, repcap.Codeword)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:RESulting:ALLoc:CW{codeword_cmd_val}:MOD?')
		return Conversions.str_to_scalar_enum(response, enums.ModType)

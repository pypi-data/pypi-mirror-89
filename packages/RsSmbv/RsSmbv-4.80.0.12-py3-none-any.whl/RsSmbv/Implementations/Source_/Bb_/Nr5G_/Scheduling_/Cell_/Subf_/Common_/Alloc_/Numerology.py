from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import enums
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Numerology:
	"""Numerology commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("numerology", core, parent)

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, allocationPerUser=repcap.AllocationPerUser.Default) -> enums.Numerology:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:COMMon:ALLoc<DIR>:NUMerology \n
		Snippet: value: enums.Numerology = driver.source.bb.nr5G.scheduling.cell.subf.common.alloc.numerology.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default, allocationPerUser = repcap.AllocationPerUser.Default) \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param allocationPerUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:return: rep_com_alloc_nume: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		allocationPerUser_cmd_val = self._base.get_repcap_cmd_value(allocationPerUser, repcap.AllocationPerUser)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:COMMon:ALLoc{allocationPerUser_cmd_val}:NUMerology?')
		return Conversions.str_to_scalar_enum(response, enums.Numerology)

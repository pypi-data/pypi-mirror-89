from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import enums
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Repetitions:
	"""Repetitions commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("repetitions", core, parent)

	def set(self, repetition: enums.RepTypeAll, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:REPetitions \n
		Snippet: driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.repetitions.set(repetition = enums.RepTypeAll.CUSTom, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Defines if and how often the allocation is repeated. \n
			:param repetition: OFF| SUBFrame| FRAMe| SLOT| CUSTom
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		param = Conversions.enum_scalar_to_str(repetition, enums.RepTypeAll)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:REPetitions {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.RepTypeAll:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:REPetitions \n
		Snippet: value: enums.RepTypeAll = driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.repetitions.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Defines if and how often the allocation is repeated. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:return: repetition: OFF| SUBFrame| FRAMe| SLOT| CUSTom"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:REPetitions?')
		return Conversions.str_to_scalar_enum(response, enums.RepTypeAll)

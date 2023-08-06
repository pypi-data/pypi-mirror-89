from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Repetitions:
	"""Repetitions commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("repetitions", core, parent)

	def set(self, repetitions: enums.EutraRepetitionsNbiot, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:NIOT:TRANs<CH>:REPetitions \n
		Snippet: driver.source.bb.eutra.ul.ue.niot.trans.repetitions.set(repetitions = enums.EutraRepetitionsNbiot.R1, stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the number of repetitions. \n
			:param repetitions: R1| R2| R4| R8| R16| R32| R64| R128
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trans')"""
		param = Conversions.enum_scalar_to_str(repetitions, enums.EutraRepetitionsNbiot)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:NIOT:TRANs{channel_cmd_val}:REPetitions {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> enums.EutraRepetitionsNbiot:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:NIOT:TRANs<CH>:REPetitions \n
		Snippet: value: enums.EutraRepetitionsNbiot = driver.source.bb.eutra.ul.ue.niot.trans.repetitions.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the number of repetitions. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trans')
			:return: repetitions: R1| R2| R4| R8| R16| R32| R64| R128"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:NIOT:TRANs{channel_cmd_val}:REPetitions?')
		return Conversions.str_to_scalar_enum(response, enums.EutraRepetitionsNbiot)

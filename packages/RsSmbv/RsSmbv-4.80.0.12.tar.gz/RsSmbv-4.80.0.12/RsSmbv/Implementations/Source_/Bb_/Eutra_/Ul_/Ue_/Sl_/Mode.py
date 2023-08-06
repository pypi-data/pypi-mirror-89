from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mode", core, parent)

	def set(self, mode: enums.EutraSlMode, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:MODE \n
		Snippet: driver.source.bb.eutra.ul.ue.sl.mode.set(mode = enums.EutraSlMode.COMM, stream = repcap.Stream.Default) \n
		Sets the mode of the sidelink communication. \n
			:param mode: COMM| DISC | V2X
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')"""
		param = Conversions.enum_scalar_to_str(mode, enums.EutraSlMode)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:SL:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.EutraSlMode:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:MODE \n
		Snippet: value: enums.EutraSlMode = driver.source.bb.eutra.ul.ue.sl.mode.get(stream = repcap.Stream.Default) \n
		Sets the mode of the sidelink communication. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: mode: COMM| DISC | V2X"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:SL:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.EutraSlMode)

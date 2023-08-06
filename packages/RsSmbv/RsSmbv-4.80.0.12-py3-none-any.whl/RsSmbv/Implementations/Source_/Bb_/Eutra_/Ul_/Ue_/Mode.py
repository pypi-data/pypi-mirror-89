from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mode", core, parent)

	def set(self, mode: enums.EutraUeMode, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:MODE \n
		Snippet: driver.source.bb.eutra.ul.ue.mode.set(mode = enums.EutraUeMode.PRACh, stream = repcap.Stream.Default) \n
		Selects whether the user equipment is in standard or in PRACH mode. \n
			:param mode: STD| PRACh
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')"""
		param = Conversions.enum_scalar_to_str(mode, enums.EutraUeMode)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.EutraUeMode:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:MODE \n
		Snippet: value: enums.EutraUeMode = driver.source.bb.eutra.ul.ue.mode.get(stream = repcap.Stream.Default) \n
		Selects whether the user equipment is in standard or in PRACH mode. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: mode: STD| PRACh"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.EutraUeMode)

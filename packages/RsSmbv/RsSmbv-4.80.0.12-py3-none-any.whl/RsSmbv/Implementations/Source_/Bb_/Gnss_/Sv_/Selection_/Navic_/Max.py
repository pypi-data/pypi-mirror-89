from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Max:
	"""Max commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("max", core, parent)

	def set(self, maximum_sv_s: int, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SV:SELection:NAVic<ST>:MAX \n
		Snippet: driver.source.bb.gnss.sv.selection.navic.max.set(maximum_sv_s = 1, stream = repcap.Stream.Default) \n
		Sets the minimum and maximum number of satellites per GNSS system that can be included in the satellite constellation. \n
			:param maximum_sv_s: integer Range: 0 to 24
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Navic')"""
		param = Conversions.decimal_value_to_str(maximum_sv_s)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SV:SELection:NAVic{stream_cmd_val}:MAX {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SV:SELection:NAVic<ST>:MAX \n
		Snippet: value: int = driver.source.bb.gnss.sv.selection.navic.max.get(stream = repcap.Stream.Default) \n
		Sets the minimum and maximum number of satellites per GNSS system that can be included in the satellite constellation. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Navic')
			:return: maximum_sv_s: integer Range: 0 to 24"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SV:SELection:NAVic{stream_cmd_val}:MAX?')
		return Conversions.str_to_int(response)

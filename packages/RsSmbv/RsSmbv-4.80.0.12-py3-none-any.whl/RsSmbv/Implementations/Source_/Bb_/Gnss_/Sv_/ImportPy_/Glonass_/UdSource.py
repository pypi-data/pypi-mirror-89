from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UdSource:
	"""UdSource commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("udSource", core, parent)

	def set(self, use_diff_src_state: bool, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SV:IMPort:GLONass<ST>:UDSource \n
		Snippet: driver.source.bb.gnss.sv.importPy.glonass.udSource.set(use_diff_src_state = False, stream = repcap.Stream.Default) \n
		Enables loading the dedicated files as source for the navigation data. \n
			:param use_diff_src_state: 0| 1| OFF| ON
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Glonass')"""
		param = Conversions.bool_to_str(use_diff_src_state)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SV:IMPort:GLONass{stream_cmd_val}:UDSource {param}')

	def get(self, stream=repcap.Stream.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SV:IMPort:GLONass<ST>:UDSource \n
		Snippet: value: bool = driver.source.bb.gnss.sv.importPy.glonass.udSource.get(stream = repcap.Stream.Default) \n
		Enables loading the dedicated files as source for the navigation data. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Glonass')
			:return: use_diff_src_state: 0| 1| OFF| ON"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SV:IMPort:GLONass{stream_cmd_val}:UDSource?')
		return Conversions.str_to_bool(response)

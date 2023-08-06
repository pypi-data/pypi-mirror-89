from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ToWeek:
	"""ToWeek commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("toWeek", core, parent)

	def get(self, stream=repcap.Stream.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TIME:STARt:GPS<ST>:TOWeek \n
		Snippet: value: float = driver.source.bb.gnss.time.start.gps.toWeek.get(stream = repcap.Stream.Default) \n
		Queries the time of week at the simulation start of the selected navigation standard. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')
			:return: tow: float Range: 0 to 604799.999"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:TIME:STARt:GPS{stream_cmd_val}:TOWeek?')
		return Conversions.str_to_float(response)

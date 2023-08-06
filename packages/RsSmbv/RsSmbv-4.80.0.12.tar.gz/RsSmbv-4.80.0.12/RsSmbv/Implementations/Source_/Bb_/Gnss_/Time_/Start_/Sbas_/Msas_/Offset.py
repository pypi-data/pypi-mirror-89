from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Offset:
	"""Offset commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("offset", core, parent)

	def get(self, stream=repcap.Stream.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TIME:STARt:SBAS<ST>:MSAS:OFFSet \n
		Snippet: value: float = driver.source.bb.gnss.time.start.sbas.msas.offset.get(stream = repcap.Stream.Default) \n
		Queries the time offset between the time in the navigation standard and UTC. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbas')
			:return: utc_offset: float Range: -1E6 to 1E6"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:TIME:STARt:SBAS{stream_cmd_val}:MSAS:OFFSet?')
		return Conversions.str_to_float(response)

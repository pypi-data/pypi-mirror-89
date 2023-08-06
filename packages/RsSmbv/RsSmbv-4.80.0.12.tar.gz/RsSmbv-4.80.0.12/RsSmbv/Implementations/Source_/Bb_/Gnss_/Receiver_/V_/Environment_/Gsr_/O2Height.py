from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class O2Height:
	"""O2Height commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("o2Height", core, parent)

	def set(self, height: float, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ENVironment:GSR:O2Height \n
		Snippet: driver.source.bb.gnss.receiver.v.environment.gsr.o2Height.set(height = 1.0, stream = repcap.Stream.Default) \n
		Determines the height of the left/right obstacle. \n
			:param height: float Range: 0 to 10000
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')"""
		param = Conversions.decimal_value_to_str(height)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:ENVironment:GSR:O2Height {param}')

	def get(self, stream=repcap.Stream.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ENVironment:GSR:O2Height \n
		Snippet: value: float = driver.source.bb.gnss.receiver.v.environment.gsr.o2Height.get(stream = repcap.Stream.Default) \n
		Determines the height of the left/right obstacle. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:return: height: float Range: 0 to 10000"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:ENVironment:GSR:O2Height?')
		return Conversions.str_to_float(response)

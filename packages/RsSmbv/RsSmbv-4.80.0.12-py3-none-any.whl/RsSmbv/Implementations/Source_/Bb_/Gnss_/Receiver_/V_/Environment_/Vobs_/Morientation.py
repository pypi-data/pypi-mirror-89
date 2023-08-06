from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Morientation:
	"""Morientation commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("morientation", core, parent)

	def set(self, map_orientation: float, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ENVironment:VOBS:MORientation \n
		Snippet: driver.source.bb.gnss.receiver.v.environment.vobs.morientation.set(map_orientation = 1.0, stream = repcap.Stream.Default) \n
		Defines the map orientation of obstacles relative to the west-east axis. \n
			:param map_orientation: float Range: 0 to 359.99
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')"""
		param = Conversions.decimal_value_to_str(map_orientation)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:ENVironment:VOBS:MORientation {param}')

	def get(self, stream=repcap.Stream.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ENVironment:VOBS:MORientation \n
		Snippet: value: float = driver.source.bb.gnss.receiver.v.environment.vobs.morientation.get(stream = repcap.Stream.Default) \n
		Defines the map orientation of obstacles relative to the west-east axis. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:return: map_orientation: float Range: 0 to 359.99"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:ENVironment:VOBS:MORientation?')
		return Conversions.str_to_float(response)

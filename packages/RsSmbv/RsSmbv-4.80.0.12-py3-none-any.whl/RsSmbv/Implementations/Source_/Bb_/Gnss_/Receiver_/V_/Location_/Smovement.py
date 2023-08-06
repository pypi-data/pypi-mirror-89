from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Smovement:
	"""Smovement commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("smovement", core, parent)

	def set(self, smooth_movement: bool, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:LOCation:SMOVement \n
		Snippet: driver.source.bb.gnss.receiver.v.location.smovement.set(smooth_movement = False, stream = repcap.Stream.Default) \n
		Applies an internal algorithm to smooth the trajectory. \n
			:param smooth_movement: 0| 1| OFF| ON
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')"""
		param = Conversions.bool_to_str(smooth_movement)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:LOCation:SMOVement {param}')

	def get(self, stream=repcap.Stream.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:LOCation:SMOVement \n
		Snippet: value: bool = driver.source.bb.gnss.receiver.v.location.smovement.get(stream = repcap.Stream.Default) \n
		Applies an internal algorithm to smooth the trajectory. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:return: smooth_movement: 0| 1| OFF| ON"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:LOCation:SMOVement?')
		return Conversions.str_to_bool(response)

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, state: bool, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SYSTem:NAVic<ST>:[STATe] \n
		Snippet: driver.source.bb.gnss.system.navic.state.set(state = False, stream = repcap.Stream.Default) \n
		Defines if satellites from the selected GNSS system are included in the simulated satellites constellation. \n
			:param state: 0| 1| OFF| ON Disabling a GNSS system deactivates all SVID and signals from this system.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Navic')"""
		param = Conversions.bool_to_str(state)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SYSTem:NAVic{stream_cmd_val}:STATe {param}')

	def get(self, stream=repcap.Stream.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SYSTem:NAVic<ST>:[STATe] \n
		Snippet: value: bool = driver.source.bb.gnss.system.navic.state.get(stream = repcap.Stream.Default) \n
		Defines if satellites from the selected GNSS system are included in the simulated satellites constellation. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Navic')
			:return: state: 0| 1| OFF| ON Disabling a GNSS system deactivates all SVID and signals from this system."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SYSTem:NAVic{stream_cmd_val}:STATe?')
		return Conversions.str_to_bool(response)

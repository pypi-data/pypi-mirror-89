from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rwindow:
	"""Rwindow commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rwindow", core, parent)

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Rwindow_.State import State
			self._state = State(self._core, self._base)
		return self._state

	def set(self, rep_window: int, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ENVironment:FULL:RWINdow \n
		Snippet: driver.source.bb.gnss.receiver.v.environment.full.rwindow.set(rep_window = 1, stream = repcap.Stream.Default) \n
		Sets the repeating period (in km or s) of repeating objects. \n
			:param rep_window: integer Range: 0 to 1000
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')"""
		param = Conversions.decimal_value_to_str(rep_window)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:ENVironment:FULL:RWINdow {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ENVironment:FULL:RWINdow \n
		Snippet: value: int = driver.source.bb.gnss.receiver.v.environment.full.rwindow.get(stream = repcap.Stream.Default) \n
		Sets the repeating period (in km or s) of repeating objects. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:return: rep_window: integer Range: 0 to 1000"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:ENVironment:FULL:RWINdow?')
		return Conversions.str_to_int(response)

	def clone(self) -> 'Rwindow':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Rwindow(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

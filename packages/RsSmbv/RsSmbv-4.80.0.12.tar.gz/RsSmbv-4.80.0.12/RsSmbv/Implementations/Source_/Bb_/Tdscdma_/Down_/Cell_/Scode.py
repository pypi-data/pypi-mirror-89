from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Scode:
	"""Scode commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scode", core, parent)

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Scode_.State import State
			self._state = State(self._core, self._base)
		return self._state

	def set(self, scode: int, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:SCODe \n
		Snippet: driver.source.bb.tdscdma.down.cell.scode.set(scode = 1, stream = repcap.Stream.Default) \n
		Sets the scrambling code. The scrambling code is used for transmitter-dependent scrambling of the chip sequence. \n
			:param scode: integer Range: 0 to 127
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.decimal_value_to_str(scode)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:SCODe {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:SCODe \n
		Snippet: value: int = driver.source.bb.tdscdma.down.cell.scode.get(stream = repcap.Stream.Default) \n
		Sets the scrambling code. The scrambling code is used for transmitter-dependent scrambling of the chip sequence. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: scode: integer Range: 0 to 127"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:SCODe?')
		return Conversions.str_to_int(response)

	def clone(self) -> 'Scode':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Scode(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

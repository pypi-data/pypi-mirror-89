from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ppower:
	"""Ppower commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ppower", core, parent)

	@property
	def step(self):
		"""step commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_step'):
			from .Ppower_.Step import Step
			self._step = Step(self._core, self._base)
		return self._step

	def set(self, ppower: float, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:PRACh:PPOWer \n
		Snippet: driver.source.bb.w3Gpp.mstation.prach.ppower.set(ppower = 1.0, stream = repcap.Stream.Default) \n
		The command defines the power of the preamble component of the PRACH. If the preamble is repeated and the power increased
		with each repetition, this setting specifies the power achieved during the last repetition. \n
			:param ppower: float Range: -80 dB to 0 dB
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.decimal_value_to_str(ppower)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:PRACh:PPOWer {param}')

	def get(self, stream=repcap.Stream.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:PRACh:PPOWer \n
		Snippet: value: float = driver.source.bb.w3Gpp.mstation.prach.ppower.get(stream = repcap.Stream.Default) \n
		The command defines the power of the preamble component of the PRACH. If the preamble is repeated and the power increased
		with each repetition, this setting specifies the power achieved during the last repetition. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: ppower: float Range: -80 dB to 0 dB"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:PRACh:PPOWer?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'Ppower':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ppower(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Satellite:
	"""Satellite commands group definition. 30 total commands, 4 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("satellite", core, parent)

	@property
	def clock(self):
		"""clock commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clock'):
			from .Satellite_.Clock import Clock
			self._clock = Clock(self._core, self._base)
		return self._clock

	@property
	def filterPy(self):
		"""filterPy commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_filterPy'):
			from .Satellite_.FilterPy import FilterPy
			self._filterPy = FilterPy(self._core, self._base)
		return self._filterPy

	@property
	def symbolRate(self):
		"""symbolRate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symbolRate'):
			from .Satellite_.SymbolRate import SymbolRate
			self._symbolRate = SymbolRate(self._core, self._base)
		return self._symbolRate

	@property
	def trigger(self):
		"""trigger commands group. 3 Sub-classes, 3 commands."""
		if not hasattr(self, '_trigger'):
			from .Satellite_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	def get_delay(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:XMRadio:SATellite:DELay \n
		Snippet: value: float = driver.source.bb.xmradio.satellite.get_delay() \n
		No command help available \n
			:return: delay: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:XMRadio:SATellite:DELay?')
		return Conversions.str_to_float(response)

	def set_delay(self, delay: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:XMRadio:SATellite:DELay \n
		Snippet: driver.source.bb.xmradio.satellite.set_delay(delay = 1.0) \n
		No command help available \n
			:param delay: No help available
		"""
		param = Conversions.decimal_value_to_str(delay)
		self._core.io.write(f'SOURce<HwInstance>:BB:XMRadio:SATellite:DELay {param}')

	def clone(self) -> 'Satellite':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Satellite(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

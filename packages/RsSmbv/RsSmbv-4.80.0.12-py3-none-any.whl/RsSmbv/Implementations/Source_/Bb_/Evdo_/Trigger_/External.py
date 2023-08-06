from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class External:
	"""External commands group definition. 3 total commands, 1 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("external", core, parent)

	@property
	def synchronize(self):
		"""synchronize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_synchronize'):
			from .External_.Synchronize import Synchronize
			self._synchronize = Synchronize(self._core, self._base)
		return self._synchronize

	def get_delay(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:EVDO:TRIGger:[EXTernal]:DELay \n
		Snippet: value: float = driver.source.bb.evdo.trigger.external.get_delay() \n
		Sets the trigger delay. \n
			:return: delay: float Range: 0 to 2147483647, Unit: samples
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EVDO:TRIGger:EXTernal:DELay?')
		return Conversions.str_to_float(response)

	def set_delay(self, delay: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:EVDO:TRIGger:[EXTernal]:DELay \n
		Snippet: driver.source.bb.evdo.trigger.external.set_delay(delay = 1.0) \n
		Sets the trigger delay. \n
			:param delay: float Range: 0 to 2147483647, Unit: samples
		"""
		param = Conversions.decimal_value_to_str(delay)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:TRIGger:EXTernal:DELay {param}')

	def get_inhibit(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:EVDO:TRIGger:[EXTernal]:INHibit \n
		Snippet: value: int = driver.source.bb.evdo.trigger.external.get_inhibit() \n
		Specifies the duration by which a restart is inhibited. \n
			:return: inhibit: integer Range: 0 to 21.47*chipRate
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EVDO:TRIGger:EXTernal:INHibit?')
		return Conversions.str_to_int(response)

	def set_inhibit(self, inhibit: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:EVDO:TRIGger:[EXTernal]:INHibit \n
		Snippet: driver.source.bb.evdo.trigger.external.set_inhibit(inhibit = 1) \n
		Specifies the duration by which a restart is inhibited. \n
			:param inhibit: integer Range: 0 to 21.47*chipRate
		"""
		param = Conversions.decimal_value_to_str(inhibit)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:TRIGger:EXTernal:INHibit {param}')

	def clone(self) -> 'External':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = External(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Trigger:
	"""Trigger commands group definition. 16 total commands, 3 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("trigger", core, parent)

	@property
	def external(self):
		"""external commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_external'):
			from .Trigger_.External import External
			self._external = External(self._core, self._base)
		return self._external

	@property
	def obaseband(self):
		"""obaseband commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_obaseband'):
			from .Trigger_.Obaseband import Obaseband
			self._obaseband = Obaseband(self._core, self._base)
		return self._obaseband

	@property
	def output(self):
		"""output commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_output'):
			from .Trigger_.Output import Output
			self._output = Output(self._core, self._base)
		return self._output

	def get_slength(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:XMRadio:SATellite:TRIGger:SLENgth \n
		Snippet: value: int = driver.source.bb.xmradio.satellite.trigger.get_slength() \n
		No command help available \n
			:return: slength: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:XMRadio:SATellite:TRIGger:SLENgth?')
		return Conversions.str_to_int(response)

	def set_slength(self, slength: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:XMRadio:SATellite:TRIGger:SLENgth \n
		Snippet: driver.source.bb.xmradio.satellite.trigger.set_slength(slength = 1) \n
		No command help available \n
			:param slength: No help available
		"""
		param = Conversions.decimal_value_to_str(slength)
		self._core.io.write(f'SOURce<HwInstance>:BB:XMRadio:SATellite:TRIGger:SLENgth {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.TriggerSourceB:
		"""SCPI: [SOURce<HW>]:BB:XMRadio:SATellite:TRIGger:SOURce \n
		Snippet: value: enums.TriggerSourceB = driver.source.bb.xmradio.satellite.trigger.get_source() \n
		No command help available \n
			:return: source: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:XMRadio:SATellite:TRIGger:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.TriggerSourceB)

	def set_source(self, source: enums.TriggerSourceB) -> None:
		"""SCPI: [SOURce<HW>]:BB:XMRadio:SATellite:TRIGger:SOURce \n
		Snippet: driver.source.bb.xmradio.satellite.trigger.set_source(source = enums.TriggerSourceB.BEXTernal) \n
		No command help available \n
			:param source: No help available
		"""
		param = Conversions.enum_scalar_to_str(source, enums.TriggerSourceB)
		self._core.io.write(f'SOURce<HwInstance>:BB:XMRadio:SATellite:TRIGger:SOURce {param}')

	# noinspection PyTypeChecker
	def get_sequence(self) -> enums.DmTrigMode:
		"""SCPI: [SOURce<HW>]:BB:XMRadio:SATellite:[TRIGger]:SEQuence \n
		Snippet: value: enums.DmTrigMode = driver.source.bb.xmradio.satellite.trigger.get_sequence() \n
		No command help available \n
			:return: sequence: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:XMRadio:SATellite:TRIGger:SEQuence?')
		return Conversions.str_to_scalar_enum(response, enums.DmTrigMode)

	def set_sequence(self, sequence: enums.DmTrigMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:XMRadio:SATellite:[TRIGger]:SEQuence \n
		Snippet: driver.source.bb.xmradio.satellite.trigger.set_sequence(sequence = enums.DmTrigMode.AAUTo) \n
		No command help available \n
			:param sequence: No help available
		"""
		param = Conversions.enum_scalar_to_str(sequence, enums.DmTrigMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:XMRadio:SATellite:TRIGger:SEQuence {param}')

	def clone(self) -> 'Trigger':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Trigger(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

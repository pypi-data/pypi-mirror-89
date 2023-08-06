from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Trigger:
	"""Trigger commands group definition. 19 total commands, 5 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("trigger", core, parent)

	@property
	def arm(self):
		"""arm commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_arm'):
			from .Trigger_.Arm import Arm
			self._arm = Arm(self._core, self._base)
		return self._arm

	@property
	def delay(self):
		"""delay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_delay'):
			from .Trigger_.Delay import Delay
			self._delay = Delay(self._core, self._base)
		return self._delay

	@property
	def execute(self):
		"""execute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_execute'):
			from .Trigger_.Execute import Execute
			self._execute = Execute(self._core, self._base)
		return self._execute

	@property
	def external(self):
		"""external commands group. 1 Sub-classes, 4 commands."""
		if not hasattr(self, '_external'):
			from .Trigger_.External import External
			self._external = External(self._core, self._base)
		return self._external

	@property
	def output(self):
		"""output commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_output'):
			from .Trigger_.Output import Output
			self._output = Output(self._core, self._base)
		return self._output

	# noinspection PyTypeChecker
	def get_rmode(self) -> enums.TrigRunMode:
		"""SCPI: [SOURce<HW>]:BB:DM:TRIGger:RMODe \n
		Snippet: value: enums.TrigRunMode = driver.source.bb.dm.trigger.get_rmode() \n
		Queries the status of signal generation. \n
			:return: rm_ode: STOP| RUN
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:TRIGger:RMODe?')
		return Conversions.str_to_scalar_enum(response, enums.TrigRunMode)

	def get_slength(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:DM:TRIGger:SLENgth \n
		Snippet: value: int = driver.source.bb.dm.trigger.get_slength() \n
		Defines the length of the signal sequence to be output in the SINGle trigger mode. \n
			:return: slength: integer Range: 1 to 4294967295, Unit: symbol
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:TRIGger:SLENgth?')
		return Conversions.str_to_int(response)

	def set_slength(self, slength: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:DM:TRIGger:SLENgth \n
		Snippet: driver.source.bb.dm.trigger.set_slength(slength = 1) \n
		Defines the length of the signal sequence to be output in the SINGle trigger mode. \n
			:param slength: integer Range: 1 to 4294967295, Unit: symbol
		"""
		param = Conversions.decimal_value_to_str(slength)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:TRIGger:SLENgth {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.TriggerSourceA:
		"""SCPI: [SOURce<HW>]:BB:DM:TRIGger:SOURce \n
		Snippet: value: enums.TriggerSourceA = driver.source.bb.dm.trigger.get_source() \n
			INTRO_CMD_HELP: Selects the trigger signal source and determines the way the triggering is executed. Provided are: \n
			- Internal triggering by a command (INTernal)
			- External trigger signal via one of the User x connectors
			Table Header:  \n
			- EGT1: External global trigger
			- EGC1: External global clock
			- In master-slave mode, the external baseband synchronization signal (BBSY)
			- EXTernal: Setting only Provided only for backward compatibility with other Rohde
		& Schwarz signal generators. The R&S SMBV100B accepts this value and maps it automatically as follows: EXTernal = EGT1 \n
			:return: source: INTernal| EGT1| EGC1| EXTernal| BBSY
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:TRIGger:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.TriggerSourceA)

	def set_source(self, source: enums.TriggerSourceA) -> None:
		"""SCPI: [SOURce<HW>]:BB:DM:TRIGger:SOURce \n
		Snippet: driver.source.bb.dm.trigger.set_source(source = enums.TriggerSourceA.BBSY) \n
			INTRO_CMD_HELP: Selects the trigger signal source and determines the way the triggering is executed. Provided are: \n
			- Internal triggering by a command (INTernal)
			- External trigger signal via one of the User x connectors
			Table Header:  \n
			- EGT1: External global trigger
			- EGC1: External global clock
			- In master-slave mode, the external baseband synchronization signal (BBSY)
			- EXTernal: Setting only Provided only for backward compatibility with other Rohde
		& Schwarz signal generators. The R&S SMBV100B accepts this value and maps it automatically as follows: EXTernal = EGT1 \n
			:param source: INTernal| EGT1| EGC1| EXTernal| BBSY
		"""
		param = Conversions.enum_scalar_to_str(source, enums.TriggerSourceA)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:TRIGger:SOURce {param}')

	# noinspection PyTypeChecker
	def get_sequence(self) -> enums.DmTrigMode:
		"""SCPI: [SOURce<HW>]:BB:DM:[TRIGger]:SEQuence \n
		Snippet: value: enums.DmTrigMode = driver.source.bb.dm.trigger.get_sequence() \n
		Selects the trigger mode. For detailed description of the trigger modes, refer to 'Impact of the Trigger Modes on the
		Signal Generation'. \n
			:return: sequence: AUTO| RETRigger| AAUTo| ARETrigger| SINGle
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:TRIGger:SEQuence?')
		return Conversions.str_to_scalar_enum(response, enums.DmTrigMode)

	def set_sequence(self, sequence: enums.DmTrigMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:DM:[TRIGger]:SEQuence \n
		Snippet: driver.source.bb.dm.trigger.set_sequence(sequence = enums.DmTrigMode.AAUTo) \n
		Selects the trigger mode. For detailed description of the trigger modes, refer to 'Impact of the Trigger Modes on the
		Signal Generation'. \n
			:param sequence: AUTO| RETRigger| AAUTo| ARETrigger| SINGle
		"""
		param = Conversions.enum_scalar_to_str(sequence, enums.DmTrigMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:TRIGger:SEQuence {param}')

	def clone(self) -> 'Trigger':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Trigger(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

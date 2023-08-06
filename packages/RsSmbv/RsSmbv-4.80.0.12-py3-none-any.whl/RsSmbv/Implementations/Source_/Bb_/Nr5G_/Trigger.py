from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Trigger:
	"""Trigger commands group definition. 36 total commands, 6 Sub-groups, 5 group commands"""

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
	def obaseband(self):
		"""obaseband commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_obaseband'):
			from .Trigger_.Obaseband import Obaseband
			self._obaseband = Obaseband(self._core, self._base)
		return self._obaseband

	@property
	def output(self):
		"""output commands group. 15 Sub-classes, 0 commands."""
		if not hasattr(self, '_output'):
			from .Trigger_.Output import Output
			self._output = Output(self._core, self._base)
		return self._output

	# noinspection PyTypeChecker
	def get_rmode(self) -> enums.TrigRunMode:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TRIGger:RMODe \n
		Snippet: value: enums.TrigRunMode = driver.source.bb.nr5G.trigger.get_rmode() \n
		Queries the signal generation status. \n
			:return: trig_run_mode: STOP| RUN
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TRIGger:RMODe?')
		return Conversions.str_to_scalar_enum(response, enums.TrigRunMode)

	def get_slength(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TRIGger:SLENgth \n
		Snippet: value: int = driver.source.bb.nr5G.trigger.get_slength() \n
		Defines the length of the signal sequence that is output in the SINGle trigger mode. \n
			:return: trig_seq_len: integer Range: 1 to dynamic
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TRIGger:SLENgth?')
		return Conversions.str_to_int(response)

	def set_slength(self, trig_seq_len: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TRIGger:SLENgth \n
		Snippet: driver.source.bb.nr5G.trigger.set_slength(trig_seq_len = 1) \n
		Defines the length of the signal sequence that is output in the SINGle trigger mode. \n
			:param trig_seq_len: integer Range: 1 to dynamic
		"""
		param = Conversions.decimal_value_to_str(trig_seq_len)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TRIGger:SLENgth {param}')

	# noinspection PyTypeChecker
	def get_sl_unit(self) -> enums.UnitSlB:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TRIGger:SLUNit \n
		Snippet: value: enums.UnitSlB = driver.source.bb.nr5G.trigger.get_sl_unit() \n
		Defines the unit for the entry of the signal sequence length. \n
			:return: trig_seq_len_unit: SEQuence| SAMPle
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TRIGger:SLUNit?')
		return Conversions.str_to_scalar_enum(response, enums.UnitSlB)

	def set_sl_unit(self, trig_seq_len_unit: enums.UnitSlB) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TRIGger:SLUNit \n
		Snippet: driver.source.bb.nr5G.trigger.set_sl_unit(trig_seq_len_unit = enums.UnitSlB.SAMPle) \n
		Defines the unit for the entry of the signal sequence length. \n
			:param trig_seq_len_unit: SEQuence| SAMPle
		"""
		param = Conversions.enum_scalar_to_str(trig_seq_len_unit, enums.UnitSlB)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TRIGger:SLUNit {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.TriggerSourceC:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TRIGger:SOURce \n
		Snippet: value: enums.TriggerSourceC = driver.source.bb.nr5G.trigger.get_source() \n
			INTRO_CMD_HELP: Selects the trigger signal source and determines the way the triggering is executed. Provided are: \n
			- Internal triggering by a command (INTernal)
			- External trigger signal via one of the User x connectors
			Table Header:  \n
			- EGT1: External global trigger
			- EGC1: External global clock
			- In master-slave mode, the external baseband synchronization signal (BBSY)
			- EXTernal: Setting only Provided only for backward compatibility with other Rohde
		& Schwarz signal generators. The R&S SMBV100B accepts this value and maps it automatically as follows: EXTernal = EGT1 \n
			:return: trig_source: INTernal| EGT1| EGC1| EXTernal| BBSY
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TRIGger:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.TriggerSourceC)

	def set_source(self, trig_source: enums.TriggerSourceC) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TRIGger:SOURce \n
		Snippet: driver.source.bb.nr5G.trigger.set_source(trig_source = enums.TriggerSourceC.BBSY) \n
			INTRO_CMD_HELP: Selects the trigger signal source and determines the way the triggering is executed. Provided are: \n
			- Internal triggering by a command (INTernal)
			- External trigger signal via one of the User x connectors
			Table Header:  \n
			- EGT1: External global trigger
			- EGC1: External global clock
			- In master-slave mode, the external baseband synchronization signal (BBSY)
			- EXTernal: Setting only Provided only for backward compatibility with other Rohde
		& Schwarz signal generators. The R&S SMBV100B accepts this value and maps it automatically as follows: EXTernal = EGT1 \n
			:param trig_source: INTernal| EGT1| EGC1| EXTernal| BBSY
		"""
		param = Conversions.enum_scalar_to_str(trig_source, enums.TriggerSourceC)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TRIGger:SOURce {param}')

	# noinspection PyTypeChecker
	def get_sequence(self) -> enums.DmTrigMode:
		"""SCPI: [SOURce<HW>]:BB:NR5G:[TRIGger]:SEQuence \n
		Snippet: value: enums.DmTrigMode = driver.source.bb.nr5G.trigger.get_sequence() \n
		Sets the trigger mode. \n
			:return: trig_mode: AUTO| RETRigger| AAUTo| ARETrigger| SINGle
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TRIGger:SEQuence?')
		return Conversions.str_to_scalar_enum(response, enums.DmTrigMode)

	def set_sequence(self, trig_mode: enums.DmTrigMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:[TRIGger]:SEQuence \n
		Snippet: driver.source.bb.nr5G.trigger.set_sequence(trig_mode = enums.DmTrigMode.AAUTo) \n
		Sets the trigger mode. \n
			:param trig_mode: AUTO| RETRigger| AAUTo| ARETrigger| SINGle
		"""
		param = Conversions.enum_scalar_to_str(trig_mode, enums.DmTrigMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TRIGger:SEQuence {param}')

	def clone(self) -> 'Trigger':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Trigger(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

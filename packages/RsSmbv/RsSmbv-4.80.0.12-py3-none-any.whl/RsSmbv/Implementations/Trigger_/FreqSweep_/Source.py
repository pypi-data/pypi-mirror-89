from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Source:
	"""Source commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("source", core, parent)

	# noinspection PyTypeChecker
	def get_advanced(self) -> enums.TrigSweepImmBusExt:
		"""SCPI: TRIGger<HW>:FSWeep:SOURce:ADVanced \n
		Snippet: value: enums.TrigSweepImmBusExt = driver.trigger.freqSweep.source.get_advanced() \n
		No command help available \n
			:return: fs_trig_source_adv: No help available
		"""
		response = self._core.io.query_str('TRIGger<HwInstance>:FSWeep:SOURce:ADVanced?')
		return Conversions.str_to_scalar_enum(response, enums.TrigSweepImmBusExt)

	def set_advanced(self, fs_trig_source_adv: enums.TrigSweepImmBusExt) -> None:
		"""SCPI: TRIGger<HW>:FSWeep:SOURce:ADVanced \n
		Snippet: driver.trigger.freqSweep.source.set_advanced(fs_trig_source_adv = enums.TrigSweepImmBusExt.BUS) \n
		No command help available \n
			:param fs_trig_source_adv: No help available
		"""
		param = Conversions.enum_scalar_to_str(fs_trig_source_adv, enums.TrigSweepImmBusExt)
		self._core.io.write(f'TRIGger<HwInstance>:FSWeep:SOURce:ADVanced {param}')

	# noinspection PyTypeChecker
	def get_value(self) -> enums.SingExtAuto:
		"""SCPI: TRIGger<HW>:FSWeep:SOURce \n
		Snippet: value: enums.SingExtAuto = driver.trigger.freqSweep.source.get_value() \n
			INTRO_CMD_HELP: Selects the trigger source for the corresponding sweeps: \n
			- FSWeep - RF frequency
			- LFFSweep - LF frequency
			- PSWeep - RF level
			- SWEep - all sweeps
		The source names of the parameters correspond to the values provided in manual control of the instrument. They differ
		from the SCPI-compliant names, but the instrument accepts both variants. Use the SCPI name, if compatibility is an
		important issue. Find the corresponding SCPI-compliant commands in Cross-reference between the manual and remote control. \n
			:return: source: AUTO| IMMediate | SINGle| BUS | EXTernal | EAUTo AUTO [IMMediate] Executes a sweep automatically. In this free-running mode, the trigger condition is met continuously. I.e. when a sweep is completed, the next one starts immediately. SINGle [BUS] Executes one complete sweep cycle. The following commands initiate a trigger event: *TRG method RsSmbv.Source.Sweep.Power.Execute.set EXECute :​TRIGgerhw[:​SWEep][:​IMMediate], method RsSmbv.Trigger.Sweep.Immediate.set and method RsSmbv.Trigger.Sweep.Immediate.set. Set the sweep mode with the commands: method RsSmbv.Source.Sweep.Power.Mode.valueAUTO|STEP MODEAUTO|STEP LFOutput:MODEAUTO|STEP In step mode (STEP) , the instrument executes only one step. EXTernal An external signal triggers the sweep. EAUTo An external signal triggers the sweep. When one sweep is finished, the next sweep starts. A second trigger event stops the sweep at the current frequency, a third trigger event starts the trigger at the start frequency, and so on.
		"""
		response = self._core.io.query_str('TRIGger<HwInstance>:FSWeep:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.SingExtAuto)

	def set_value(self, source: enums.SingExtAuto) -> None:
		"""SCPI: TRIGger<HW>:FSWeep:SOURce \n
		Snippet: driver.trigger.freqSweep.source.set_value(source = enums.SingExtAuto.AUTO) \n
			INTRO_CMD_HELP: Selects the trigger source for the corresponding sweeps: \n
			- FSWeep - RF frequency
			- LFFSweep - LF frequency
			- PSWeep - RF level
			- SWEep - all sweeps
		The source names of the parameters correspond to the values provided in manual control of the instrument. They differ
		from the SCPI-compliant names, but the instrument accepts both variants. Use the SCPI name, if compatibility is an
		important issue. Find the corresponding SCPI-compliant commands in Cross-reference between the manual and remote control. \n
			:param source: AUTO| IMMediate | SINGle| BUS | EXTernal | EAUTo AUTO [IMMediate] Executes a sweep automatically. In this free-running mode, the trigger condition is met continuously. I.e. when a sweep is completed, the next one starts immediately. SINGle [BUS] Executes one complete sweep cycle. The following commands initiate a trigger event: *TRG method RsSmbv.Source.Sweep.Power.Execute.set EXECute :​TRIGgerhw[:​SWEep][:​IMMediate], method RsSmbv.Trigger.Sweep.Immediate.set and method RsSmbv.Trigger.Sweep.Immediate.set. Set the sweep mode with the commands: method RsSmbv.Source.Sweep.Power.Mode.valueAUTO|STEP MODEAUTO|STEP LFOutput:MODEAUTO|STEP In step mode (STEP) , the instrument executes only one step. EXTernal An external signal triggers the sweep. EAUTo An external signal triggers the sweep. When one sweep is finished, the next sweep starts. A second trigger event stops the sweep at the current frequency, a third trigger event starts the trigger at the start frequency, and so on.
		"""
		param = Conversions.enum_scalar_to_str(source, enums.SingExtAuto)
		self._core.io.write(f'TRIGger<HwInstance>:FSWeep:SOURce {param}')

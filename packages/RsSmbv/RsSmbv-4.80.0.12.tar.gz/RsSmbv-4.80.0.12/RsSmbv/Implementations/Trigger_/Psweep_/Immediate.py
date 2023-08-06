from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Immediate:
	"""Immediate commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("immediate", core, parent)

	def set(self) -> None:
		"""SCPI: TRIGger<HW>:PSWeep:[IMMediate] \n
		Snippet: driver.trigger.psweep.immediate.set() \n
			INTRO_CMD_HELP: Performs a single sweep and immediately starts the activated, corresponding sweep: \n
			- FSWeep - RF frequency
			- PSWeep - RF level
			- LFFSweep - LF frequency
			- SWEep - all sweeps
			INTRO_CMD_HELP: Effective in the following configuration: \n
			- TRIG:FSW|LFFS|PSW|[:SWE]:SOURSING
			- SOUR:SWE:FREQ|POW:MODEAUTO or method RsSmbv.Source.LfOutput.Sweep.Frequency.Mode.valueAUTO
		Alternatively, you can use the IMMediate command instead of the respective SWEep:[FREQ:]|POW:EXECute command. \n
		"""
		self._core.io.write(f'TRIGger<HwInstance>:PSWeep:IMMediate')

	def set_with_opc(self) -> None:
		"""SCPI: TRIGger<HW>:PSWeep:[IMMediate] \n
		Snippet: driver.trigger.psweep.immediate.set_with_opc() \n
			INTRO_CMD_HELP: Performs a single sweep and immediately starts the activated, corresponding sweep: \n
			- FSWeep - RF frequency
			- PSWeep - RF level
			- LFFSweep - LF frequency
			- SWEep - all sweeps
			INTRO_CMD_HELP: Effective in the following configuration: \n
			- TRIG:FSW|LFFS|PSW|[:SWE]:SOURSING
			- SOUR:SWE:FREQ|POW:MODEAUTO or method RsSmbv.Source.LfOutput.Sweep.Frequency.Mode.valueAUTO
		Alternatively, you can use the IMMediate command instead of the respective SWEep:[FREQ:]|POW:EXECute command. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'TRIGger<HwInstance>:PSWeep:IMMediate')

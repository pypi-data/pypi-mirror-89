from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	# noinspection PyTypeChecker
	def get_pon(self) -> enums.UnchOff:
		"""SCPI: OUTPut<HW>:[STATe]:PON \n
		Snippet: value: enums.UnchOff = driver.output.state.get_pon() \n
		Defines the state of the RF output signal when the instrument is switched on. \n
			:return: pon: OFF| UNCHanged
		"""
		response = self._core.io.query_str('OUTPut<HwInstance>:STATe:PON?')
		return Conversions.str_to_scalar_enum(response, enums.UnchOff)

	def set_pon(self, pon: enums.UnchOff) -> None:
		"""SCPI: OUTPut<HW>:[STATe]:PON \n
		Snippet: driver.output.state.set_pon(pon = enums.UnchOff.OFF) \n
		Defines the state of the RF output signal when the instrument is switched on. \n
			:param pon: OFF| UNCHanged
		"""
		param = Conversions.enum_scalar_to_str(pon, enums.UnchOff)
		self._core.io.write(f'OUTPut<HwInstance>:STATe:PON {param}')

	def get_value(self) -> bool:
		"""SCPI: OUTPut<HW>:[STATe] \n
		Snippet: value: bool = driver.output.state.get_value() \n
		Activates the RF output signal. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('OUTPut<HwInstance>:STATe?')
		return Conversions.str_to_bool(response)

	def set_value(self, state: bool) -> None:
		"""SCPI: OUTPut<HW>:[STATe] \n
		Snippet: driver.output.state.set_value(state = False) \n
		Activates the RF output signal. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'OUTPut<HwInstance>:STATe {param}')

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ocns:
	"""Ocns commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ocns", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.OcnsMode:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation:OCNS:MODE \n
		Snippet: value: enums.OcnsMode = driver.source.bb.w3Gpp.bstation.ocns.get_mode() \n
		Selects the scenario for setting the OCNS channels. To activate the selected scenario, send the command method RsSmbv.
		Source.Bb.W3Gpp.Bstation.Ocns.state. \n
			:return: mode: STANdard| HSDPa| HSDP2| M3I Four different OCNS scenarios are defined in the standard; one standard scenario, two scenarios for testing HSDPA channels and one for enhanced performance type 3i tests.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:BSTation:OCNS:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.OcnsMode)

	def set_mode(self, mode: enums.OcnsMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation:OCNS:MODE \n
		Snippet: driver.source.bb.w3Gpp.bstation.ocns.set_mode(mode = enums.OcnsMode.HSDP2) \n
		Selects the scenario for setting the OCNS channels. To activate the selected scenario, send the command method RsSmbv.
		Source.Bb.W3Gpp.Bstation.Ocns.state. \n
			:param mode: STANdard| HSDPa| HSDP2| M3I Four different OCNS scenarios are defined in the standard; one standard scenario, two scenarios for testing HSDPA channels and one for enhanced performance type 3i tests.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.OcnsMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation:OCNS:MODE {param}')

	def get_seed(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation:OCNS:SEED \n
		Snippet: value: int = driver.source.bb.w3Gpp.bstation.ocns.get_seed() \n
		In '3i' OCNS mode, sets the seed for both the random processes, the power control simulation process and the process
		controlling the switch over of the channelization codes. \n
			:return: seed: integer Range: 0 to 65535
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:BSTation:OCNS:SEED?')
		return Conversions.str_to_int(response)

	def set_seed(self, seed: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation:OCNS:SEED \n
		Snippet: driver.source.bb.w3Gpp.bstation.ocns.set_seed(seed = 1) \n
		In '3i' OCNS mode, sets the seed for both the random processes, the power control simulation process and the process
		controlling the switch over of the channelization codes. \n
			:param seed: integer Range: 0 to 65535
		"""
		param = Conversions.decimal_value_to_str(seed)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation:OCNS:SEED {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation:OCNS:STATe \n
		Snippet: value: bool = driver.source.bb.w3Gpp.bstation.ocns.get_state() \n
		Activates OCNS channels according to the scenario selected with the command method RsSmbv.Source.Bb.W3Gpp.Bstation.Ocns.
		mode. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:BSTation:OCNS:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation:OCNS:STATe \n
		Snippet: driver.source.bb.w3Gpp.bstation.ocns.set_state(state = False) \n
		Activates OCNS channels according to the scenario selected with the command method RsSmbv.Source.Bb.W3Gpp.Bstation.Ocns.
		mode. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation:OCNS:STATe {param}')

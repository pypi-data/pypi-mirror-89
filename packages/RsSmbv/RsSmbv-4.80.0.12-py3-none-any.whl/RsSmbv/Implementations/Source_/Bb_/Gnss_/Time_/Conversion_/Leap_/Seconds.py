from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Seconds:
	"""Seconds commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("seconds", core, parent)

	def get_after(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TIME:CONVersion:LEAP:SEConds:AFTer \n
		Snippet: value: int = driver.source.bb.gnss.time.conversion.leap.seconds.get_after() \n
		Specifies the leap second value after the leap second transition. \n
			:return: leap_seconds: integer Range: 0 to 50
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:TIME:CONVersion:LEAP:SEConds:AFTer?')
		return Conversions.str_to_int(response)

	def set_after(self, leap_seconds: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TIME:CONVersion:LEAP:SEConds:AFTer \n
		Snippet: driver.source.bb.gnss.time.conversion.leap.seconds.set_after(leap_seconds = 1) \n
		Specifies the leap second value after the leap second transition. \n
			:param leap_seconds: integer Range: 0 to 50
		"""
		param = Conversions.decimal_value_to_str(leap_seconds)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:TIME:CONVersion:LEAP:SEConds:AFTer {param}')

	def get_before(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TIME:CONVersion:LEAP:SEConds:BEFore \n
		Snippet: value: int = driver.source.bb.gnss.time.conversion.leap.seconds.get_before() \n
		Specifies the leap second value before the leap second transition. \n
			:return: leap_secends: integer Range: 0 to 50
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:TIME:CONVersion:LEAP:SEConds:BEFore?')
		return Conversions.str_to_int(response)

	def set_before(self, leap_secends: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TIME:CONVersion:LEAP:SEConds:BEFore \n
		Snippet: driver.source.bb.gnss.time.conversion.leap.seconds.set_before(leap_secends = 1) \n
		Specifies the leap second value before the leap second transition. \n
			:param leap_secends: integer Range: 0 to 50
		"""
		param = Conversions.decimal_value_to_str(leap_secends)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:TIME:CONVersion:LEAP:SEConds:BEFore {param}')

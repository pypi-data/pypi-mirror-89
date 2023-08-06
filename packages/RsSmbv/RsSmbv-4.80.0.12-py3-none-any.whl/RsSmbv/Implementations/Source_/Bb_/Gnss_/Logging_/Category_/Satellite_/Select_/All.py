from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class All:
	"""All commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("all", core, parent)

	def set(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:LOGGing:CATegory:SATellite:SELect:ALL \n
		Snippet: driver.source.bb.gnss.logging.category.satellite.select.all.set() \n
		Enables or disables all of the available SV IDs. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:LOGGing:CATegory:SATellite:SELect:ALL')

	def set_with_opc(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:LOGGing:CATegory:SATellite:SELect:ALL \n
		Snippet: driver.source.bb.gnss.logging.category.satellite.select.all.set_with_opc() \n
		Enables or disables all of the available SV IDs. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:GNSS:LOGGing:CATegory:SATellite:SELect:ALL')

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Force:
	"""Force commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("force", core, parent)

	def set(self) -> None:
		"""SCPI: CALibration<HW>:DATA:UPDate:LEVel:FORCe \n
		Snippet: driver.calibration.data.update.level.force.set() \n
		No command help available \n
		"""
		self._core.io.write(f'CALibration<HwInstance>:DATA:UPDate:LEVel:FORCe')

	def set_with_opc(self) -> None:
		"""SCPI: CALibration<HW>:DATA:UPDate:LEVel:FORCe \n
		Snippet: driver.calibration.data.update.level.force.set_with_opc() \n
		No command help available \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'CALibration<HwInstance>:DATA:UPDate:LEVel:FORCe')

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Output:
	"""Output commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("output", core, parent)

	def reset(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:OSTReams:OUTPut:RESet \n
		Snippet: driver.source.bb.gnss.ostreams.output.reset() \n
		No command help available \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:OSTReams:OUTPut:RESet')

	def reset_with_opc(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:OSTReams:OUTPut:RESet \n
		Snippet: driver.source.bb.gnss.ostreams.output.reset_with_opc() \n
		No command help available \n
		Same as reset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:GNSS:OSTReams:OUTPut:RESet')

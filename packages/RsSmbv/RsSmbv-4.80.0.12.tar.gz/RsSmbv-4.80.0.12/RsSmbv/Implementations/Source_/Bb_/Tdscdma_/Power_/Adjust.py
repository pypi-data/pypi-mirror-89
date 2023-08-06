from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Adjust:
	"""Adjust commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("adjust", core, parent)

	def set(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:POWer:ADJust \n
		Snippet: driver.source.bb.tdscdma.power.adjust.set() \n
		The command sets the power of the active channels in such a way that the total power of the active channels is 0 dB. This
		will not change the power ratio among the individual channels. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:POWer:ADJust')

	def set_with_opc(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:POWer:ADJust \n
		Snippet: driver.source.bb.tdscdma.power.adjust.set_with_opc() \n
		The command sets the power of the active channels in such a way that the total power of the active channels is 0 dB. This
		will not change the power ratio among the individual channels. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:TDSCdma:POWer:ADJust')

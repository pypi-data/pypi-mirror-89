from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Create:
	"""Create commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("create", core, parent)

	def set(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:TSIGnal:SINE:CREate \n
		Snippet: driver.source.bb.arbitrary.tsignal.sine.create.set() \n
		Generates a signal and uses it as output straight away. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:TSIGnal:SINE:CREate')

	def set_with_opc(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:TSIGnal:SINE:CREate \n
		Snippet: driver.source.bb.arbitrary.tsignal.sine.create.set_with_opc() \n
		Generates a signal and uses it as output straight away. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:ARBitrary:TSIGnal:SINE:CREate')

	def set_named(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:TSIGnal:SINE:CREate:NAMed \n
		Snippet: driver.source.bb.arbitrary.tsignal.sine.create.set_named(filename = '1') \n
		Generates a signal and saves it to a waveform file. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:TSIGnal:SINE:CREate:NAMed {param}')

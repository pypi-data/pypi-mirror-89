from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Synchronize:
	"""Synchronize commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("synchronize", core, parent)

	def set(self, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GALileo<ST>:SYNChronize \n
		Snippet: driver.source.bb.gnss.adGeneration.galileo.synchronize.set(stream = repcap.Stream.Default) \n
		Synchronizes the affected parameters. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Galileo')"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:GALileo{stream_cmd_val}:SYNChronize')

	def set_with_opc(self, stream=repcap.Stream.Default) -> None:
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GALileo<ST>:SYNChronize \n
		Snippet: driver.source.bb.gnss.adGeneration.galileo.synchronize.set_with_opc(stream = repcap.Stream.Default) \n
		Synchronizes the affected parameters. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Galileo')"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:GALileo{stream_cmd_val}:SYNChronize')

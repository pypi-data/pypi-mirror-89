from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Execute:
	"""Execute commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("execute", core, parent)

	def set(self, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SV:IMPort:GLONass<ST>:EXECute \n
		Snippet: driver.source.bb.gnss.sv.importPy.glonass.execute.set(stream = repcap.Stream.Default) \n
		Triggers the import of constellation and navigation data from the selected files. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Glonass')"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SV:IMPort:GLONass{stream_cmd_val}:EXECute')

	def set_with_opc(self, stream=repcap.Stream.Default) -> None:
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		"""SCPI: [SOURce<HW>]:BB:GNSS:SV:IMPort:GLONass<ST>:EXECute \n
		Snippet: driver.source.bb.gnss.sv.importPy.glonass.execute.set_with_opc(stream = repcap.Stream.Default) \n
		Triggers the import of constellation and navigation data from the selected files. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Glonass')"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:GNSS:SV:IMPort:GLONass{stream_cmd_val}:EXECute')

from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Up:
	"""Up commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("up", core, parent)

	def set(self, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PDCCh:EXTC:UP \n
		Snippet: driver.source.bb.eutra.dl.subf.encc.pdcch.extc.up.set(stream = repcap.Stream.Default) \n
		Moves the selected row down or up. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PDCCh:EXTC:UP')

	def set_with_opc(self, stream=repcap.Stream.Default) -> None:
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PDCCh:EXTC:UP \n
		Snippet: driver.source.bb.eutra.dl.subf.encc.pdcch.extc.up.set_with_opc(stream = repcap.Stream.Default) \n
		Moves the selected row down or up. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PDCCh:EXTC:UP')

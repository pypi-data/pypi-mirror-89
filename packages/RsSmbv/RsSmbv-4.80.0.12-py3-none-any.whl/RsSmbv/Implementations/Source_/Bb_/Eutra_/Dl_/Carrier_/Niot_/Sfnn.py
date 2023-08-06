from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sfnn:
	"""Sfnn commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sfnn", core, parent)

	def set(self, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:CARRier<CH>:NIOT:SFNN \n
		Snippet: driver.source.bb.eutra.dl.carrier.niot.sfnn.set(channel = repcap.Channel.Default) \n
		Sets all SFs to invalid. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Carrier')"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:CARRier{channel_cmd_val}:NIOT:SFNN')

	def set_with_opc(self, channel=repcap.Channel.Default) -> None:
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:CARRier<CH>:NIOT:SFNN \n
		Snippet: driver.source.bb.eutra.dl.carrier.niot.sfnn.set_with_opc(channel = repcap.Channel.Default) \n
		Sets all SFs to invalid. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Carrier')"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:EUTRa:DL:CARRier{channel_cmd_val}:NIOT:SFNN')

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dlist:
	"""Dlist commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dlist", core, parent)

	def set(self, usch_data_list: str, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:USCH:DLISt \n
		Snippet: driver.source.bb.nr5G.ubwp.user.usch.dlist.set(usch_data_list = '1', channel = repcap.Channel.Default) \n
		Selects an existing data list file from the default directory or from the specific directory. Refer to 'Accessing Files
		in the Default or Specified Directory' for general information on file handling in the default and in a specific
		directory. \n
			:param usch_data_list: string Filename incl. file extension or complete file path
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.value_to_quoted_str(usch_data_list)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:USCH:DLISt {param}')

	def get(self, channel=repcap.Channel.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:USCH:DLISt \n
		Snippet: value: str = driver.source.bb.nr5G.ubwp.user.usch.dlist.get(channel = repcap.Channel.Default) \n
		Selects an existing data list file from the default directory or from the specific directory. Refer to 'Accessing Files
		in the Default or Specified Directory' for general information on file handling in the default and in a specific
		directory. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: usch_data_list: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:USCH:DLISt?')
		return trim_str_response(response)

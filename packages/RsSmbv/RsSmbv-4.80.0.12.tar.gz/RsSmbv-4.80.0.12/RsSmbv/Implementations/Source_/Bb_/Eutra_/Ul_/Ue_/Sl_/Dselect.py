from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dselect:
	"""Dselect commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dselect", core, parent)

	def set(self, data_list: str, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:DSELect \n
		Snippet: driver.source.bb.eutra.ul.ue.sl.dselect.set(data_list = '1', stream = repcap.Stream.Default) \n
		Selects an existing data list file from the default directory or from the specific directory. Refer to 'Accessing Files
		in the Default or Specified Directory' for general information on file handling in the default and in a specific
		directory. \n
			:param data_list: string Filename incl. file extension or complete file path
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')"""
		param = Conversions.value_to_quoted_str(data_list)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:SL:DSELect {param}')

	def get(self, stream=repcap.Stream.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:DSELect \n
		Snippet: value: str = driver.source.bb.eutra.ul.ue.sl.dselect.get(stream = repcap.Stream.Default) \n
		Selects an existing data list file from the default directory or from the specific directory. Refer to 'Accessing Files
		in the Default or Specified Directory' for general information on file handling in the default and in a specific
		directory. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: data_list: string Filename incl. file extension or complete file path"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:SL:DSELect?')
		return trim_str_response(response)

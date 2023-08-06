from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Select:
	"""Select commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("select", core, parent)

	def set(self, freq_corr_rf_fl_sel: str, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:CORRection:FRESponse:RF:USER:FLISt<CH>:SELect \n
		Snippet: driver.source.correction.fresponse.rf.user.flist.select.set(freq_corr_rf_fl_sel = '1', channel = repcap.Channel.Default) \n
		Selects an existing frequency response list file (*.uco or *.fres) from the default directory or from the specific
		directory. Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in
		the default and in a specific directory. \n
			:param freq_corr_rf_fl_sel: string Filename incl. file extension or complete file path Use 'none' to unload a file.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')"""
		param = Conversions.value_to_quoted_str(freq_corr_rf_fl_sel)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:FRESponse:RF:USER:FLISt{channel_cmd_val}:SELect {param}')

	def get(self, channel=repcap.Channel.Default) -> str:
		"""SCPI: [SOURce<HW>]:CORRection:FRESponse:RF:USER:FLISt<CH>:SELect \n
		Snippet: value: str = driver.source.correction.fresponse.rf.user.flist.select.get(channel = repcap.Channel.Default) \n
		Selects an existing frequency response list file (*.uco or *.fres) from the default directory or from the specific
		directory. Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in
		the default and in a specific directory. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')
			:return: freq_corr_rf_fl_sel: string Filename incl. file extension or complete file path Use 'none' to unload a file."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:CORRection:FRESponse:RF:USER:FLISt{channel_cmd_val}:SELect?')
		return trim_str_response(response)

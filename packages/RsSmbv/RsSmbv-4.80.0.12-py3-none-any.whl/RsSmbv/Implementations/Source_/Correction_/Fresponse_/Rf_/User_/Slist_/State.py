from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, freq_resp_sli_stat: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:CORRection:FRESponse:RF:USER:SLISt<CH>:[STATe] \n
		Snippet: driver.source.correction.fresponse.rf.user.slist.state.set(freq_resp_sli_stat = False, channel = repcap.Channel.Default) \n
		Enables that the selected file is used for frequency response compensation. To trigger calculation of the correction
		values, send the command method RsSmbv.Source.Correction.Fresponse.Rf.User.Apply.set. Otherwise changes are not
		considered. \n
			:param freq_resp_sli_stat: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')"""
		param = Conversions.bool_to_str(freq_resp_sli_stat)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:FRESponse:RF:USER:SLISt{channel_cmd_val}:STATe {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:CORRection:FRESponse:RF:USER:SLISt<CH>:[STATe] \n
		Snippet: value: bool = driver.source.correction.fresponse.rf.user.slist.state.get(channel = repcap.Channel.Default) \n
		Enables that the selected file is used for frequency response compensation. To trigger calculation of the correction
		values, send the command method RsSmbv.Source.Correction.Fresponse.Rf.User.Apply.set. Otherwise changes are not
		considered. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')
			:return: freq_resp_sli_stat: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:CORRection:FRESponse:RF:USER:SLISt{channel_cmd_val}:STATe?')
		return Conversions.str_to_bool(response)

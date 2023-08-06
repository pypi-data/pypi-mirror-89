from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Data:
	"""Data commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("data", core, parent)

	def set(self, usch_data_source: enums.DataSour, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:USCH:DATA \n
		Snippet: driver.source.bb.nr5G.ubwp.user.usch.data.set(usch_data_source = enums.DataSour.DLISt, channel = repcap.Channel.Default) \n
		Sets the DSCH/USCH data source. \n
			:param usch_data_source: PN9| PN11| PN15| PN16| PN20| PN21| PN23| PATTern| DLISt| ZERO| ONE
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.enum_scalar_to_str(usch_data_source, enums.DataSour)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:USCH:DATA {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.DataSour:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:USCH:DATA \n
		Snippet: value: enums.DataSour = driver.source.bb.nr5G.ubwp.user.usch.data.get(channel = repcap.Channel.Default) \n
		Sets the DSCH/USCH data source. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: usch_data_source: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:USCH:DATA?')
		return Conversions.str_to_scalar_enum(response, enums.DataSour)

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Echoes:
	"""Echoes commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("echoes", core, parent)

	def set(self, show_echoes: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:MONitor<CH>:DISPlay:POWer:ECHoes \n
		Snippet: driver.source.bb.gnss.monitor.display.power.echoes.set(show_echoes = False, channel = repcap.Channel.Default) \n
		If enabled, the 'Power View' indicates also the echoes per SV. \n
			:param show_echoes: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Monitor')"""
		param = Conversions.bool_to_str(show_echoes)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:MONitor{channel_cmd_val}:DISPlay:POWer:ECHoes {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:GNSS:MONitor<CH>:DISPlay:POWer:ECHoes \n
		Snippet: value: bool = driver.source.bb.gnss.monitor.display.power.echoes.get(channel = repcap.Channel.Default) \n
		If enabled, the 'Power View' indicates also the echoes per SV. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Monitor')
			:return: show_echoes: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:MONitor{channel_cmd_val}:DISPlay:POWer:ECHoes?')
		return Conversions.str_to_bool(response)

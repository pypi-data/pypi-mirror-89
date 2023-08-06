from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ssid:
	"""Ssid commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ssid", core, parent)

	def set(self, ssid: enums.GbasSsid, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:SSID \n
		Snippet: driver.source.bb.gbas.vdb.ssid.set(ssid = enums.GbasSsid.A, channel = repcap.Channel.Default) \n
		Sets the Station Slot Identifier SSID of the ground station. \n
			:param ssid: A| B| C| D| E| F| G| H
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')"""
		param = Conversions.enum_scalar_to_str(ssid, enums.GbasSsid)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:SSID {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.GbasSsid:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:SSID \n
		Snippet: value: enums.GbasSsid = driver.source.bb.gbas.vdb.ssid.get(channel = repcap.Channel.Default) \n
		Sets the Station Slot Identifier SSID of the ground station. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:return: ssid: A| B| C| D| E| F| G| H"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:SSID?')
		return Conversions.str_to_scalar_enum(response, enums.GbasSsid)

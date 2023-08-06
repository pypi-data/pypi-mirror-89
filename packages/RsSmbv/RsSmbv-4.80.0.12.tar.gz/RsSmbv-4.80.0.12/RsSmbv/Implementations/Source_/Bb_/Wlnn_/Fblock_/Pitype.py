from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pitype:
	"""Pitype commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pitype", core, parent)

	def set(self, pi_type: enums.WlannFbPilotType, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:PITYpe \n
		Snippet: driver.source.bb.wlnn.fblock.pitype.set(pi_type = enums.WlannFbPilotType.FIXed, channel = repcap.Channel.Default) \n
		No command help available \n
			:param pi_type: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.enum_scalar_to_str(pi_type, enums.WlannFbPilotType)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:PITYpe {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.WlannFbPilotType:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:PITYpe \n
		Snippet: value: enums.WlannFbPilotType = driver.source.bb.wlnn.fblock.pitype.get(channel = repcap.Channel.Default) \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: pi_type: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:PITYpe?')
		return Conversions.str_to_scalar_enum(response, enums.WlannFbPilotType)

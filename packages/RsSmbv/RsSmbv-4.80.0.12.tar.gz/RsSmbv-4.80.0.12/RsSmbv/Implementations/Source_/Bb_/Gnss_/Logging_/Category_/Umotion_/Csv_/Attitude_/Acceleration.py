from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Acceleration:
	"""Acceleration commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("acceleration", core, parent)

	def set(self, state: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:LOGGing:CATegory:UMOTion:[CSV]:ATTitude:ACCeleration<CH> \n
		Snippet: driver.source.bb.gnss.logging.category.umotion.csv.attitude.acceleration.set(state = False, channel = repcap.Channel.Default) \n
		Enables the parameter for logging. \n
			:param state: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Attitude')"""
		param = Conversions.bool_to_str(state)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:LOGGing:CATegory:UMOTion:CSV:ATTitude:ACCeleration{channel_cmd_val} {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:GNSS:LOGGing:CATegory:UMOTion:[CSV]:ATTitude:ACCeleration<CH> \n
		Snippet: value: bool = driver.source.bb.gnss.logging.category.umotion.csv.attitude.acceleration.get(channel = repcap.Channel.Default) \n
		Enables the parameter for logging. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Attitude')
			:return: state: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:LOGGing:CATegory:UMOTion:CSV:ATTitude:ACCeleration{channel_cmd_val}?')
		return Conversions.str_to_bool(response)

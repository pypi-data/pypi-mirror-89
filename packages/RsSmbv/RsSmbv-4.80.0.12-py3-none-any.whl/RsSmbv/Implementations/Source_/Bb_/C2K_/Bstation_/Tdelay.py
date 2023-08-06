from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tdelay:
	"""Tdelay commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tdelay", core, parent)

	def set(self, tdelay: int, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:C2K:BSTation<ST>:TDELay \n
		Snippet: driver.source.bb.c2K.bstation.tdelay.set(tdelay = 1, stream = repcap.Stream.Default) \n
		Sets the time shift of the selected base station compared to base station 1. \n
			:param tdelay: integer Range: 0 to dynamic, Unit: chip
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')"""
		param = Conversions.decimal_value_to_str(tdelay)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:TDELay {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:C2K:BSTation<ST>:TDELay \n
		Snippet: value: int = driver.source.bb.c2K.bstation.tdelay.get(stream = repcap.Stream.Default) \n
		Sets the time shift of the selected base station compared to base station 1. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:return: tdelay: integer Range: 0 to dynamic, Unit: chip"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:TDELay?')
		return Conversions.str_to_int(response)

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dpty:
	"""Dpty commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dpty", core, parent)

	def set(self, dpty: bool, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:STEReo:GRPS:GT<ST>:DID:DPTY \n
		Snippet: driver.source.bb.stereo.grps.gt.did.dpty.set(dpty = False, stream = repcap.Stream.Default) \n
		No command help available \n
			:param dpty: No help available
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gt')"""
		param = Conversions.bool_to_str(dpty)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:GRPS:GT{stream_cmd_val}:DID:DPTY {param}')

	def get(self, stream=repcap.Stream.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:STEReo:GRPS:GT<ST>:DID:DPTY \n
		Snippet: value: bool = driver.source.bb.stereo.grps.gt.did.dpty.get(stream = repcap.Stream.Default) \n
		No command help available \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gt')
			:return: dpty: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:STEReo:GRPS:GT{stream_cmd_val}:DID:DPTY?')
		return Conversions.str_to_bool(response)

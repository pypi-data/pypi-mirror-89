from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PoMode:
	"""PoMode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("poMode", core, parent)

	def set(self, po_mode: enums.AutoUser, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:CMODe:POMode \n
		Snippet: driver.source.bb.w3Gpp.mstation.cmode.poMode.set(po_mode = enums.AutoUser.AUTO, stream = repcap.Stream.Default) \n
		The command selects the power offset mode. \n
			:param po_mode: AUTO| USER AUTO The power offset is obtained by pilot bit ratio as follows: Number of pilots bits of non-compressed slots / Number of pilot bits by compressed slots. USER The power offset is defined by command BB:W3GPp:CMODe:POFFset.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.enum_scalar_to_str(po_mode, enums.AutoUser)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:CMODe:POMode {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.AutoUser:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:CMODe:POMode \n
		Snippet: value: enums.AutoUser = driver.source.bb.w3Gpp.mstation.cmode.poMode.get(stream = repcap.Stream.Default) \n
		The command selects the power offset mode. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: po_mode: AUTO| USER AUTO The power offset is obtained by pilot bit ratio as follows: Number of pilots bits of non-compressed slots / Number of pilot bits by compressed slots. USER The power offset is defined by command BB:W3GPp:CMODe:POFFset."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:CMODe:POMode?')
		return Conversions.str_to_scalar_enum(response, enums.AutoUser)

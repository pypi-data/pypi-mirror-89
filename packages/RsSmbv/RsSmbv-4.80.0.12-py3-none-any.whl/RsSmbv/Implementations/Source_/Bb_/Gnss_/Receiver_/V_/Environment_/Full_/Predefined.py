from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Predefined:
	"""Predefined commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("predefined", core, parent)

	def set(self, predefined_env: enums.ObscModelFullObsc, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ENVironment:FULL:PREDefined \n
		Snippet: driver.source.bb.gnss.receiver.v.environment.full.predefined.set(predefined_env = enums.ObscModelFullObsc.BR1, stream = repcap.Stream.Default) \n
		Loads a predefined environment configuration. You can load a user-defined setting or a predefined settings that simulate
		two urban canyon environments. \n
			:param predefined_env: USER| URB1| URB2 USER User-defined environment configuration URB1|URB2 Urban canyon environment configuration
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')"""
		param = Conversions.enum_scalar_to_str(predefined_env, enums.ObscModelFullObsc)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:ENVironment:FULL:PREDefined {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.ObscModelFullObsc:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ENVironment:FULL:PREDefined \n
		Snippet: value: enums.ObscModelFullObsc = driver.source.bb.gnss.receiver.v.environment.full.predefined.get(stream = repcap.Stream.Default) \n
		Loads a predefined environment configuration. You can load a user-defined setting or a predefined settings that simulate
		two urban canyon environments. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:return: predefined_env: USER| URB1| URB2 USER User-defined environment configuration URB1|URB2 Urban canyon environment configuration"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:ENVironment:FULL:PREDefined?')
		return Conversions.str_to_scalar_enum(response, enums.ObscModelFullObsc)

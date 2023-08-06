from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Scale:
	"""Scale commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scale", core, parent)

	def set(self, scale: enums.IqOutEnvScale, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:IQ:DOHerty<ST>:SCALe \n
		Snippet: driver.source.iq.doherty.scale.set(scale = enums.IqOutEnvScale.POWer, stream = repcap.Stream.Default) \n
		No command help available \n
			:param scale: No help available
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Doherty')"""
		param = Conversions.enum_scalar_to_str(scale, enums.IqOutEnvScale)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:IQ:DOHerty{stream_cmd_val}:SCALe {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.IqOutEnvScale:
		"""SCPI: [SOURce<HW>]:IQ:DOHerty<ST>:SCALe \n
		Snippet: value: enums.IqOutEnvScale = driver.source.iq.doherty.scale.get(stream = repcap.Stream.Default) \n
		No command help available \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Doherty')
			:return: scale: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:IQ:DOHerty{stream_cmd_val}:SCALe?')
		return Conversions.str_to_scalar_enum(response, enums.IqOutEnvScale)

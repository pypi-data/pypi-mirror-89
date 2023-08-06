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
		"""SCPI: [SOURce<HW>]:IQ:DPD<ST>:SCALe \n
		Snippet: driver.source.iq.dpd.scale.set(scale = enums.IqOutEnvScale.POWer, stream = repcap.Stream.Default) \n
		Determines the units used on the x and y-axis. \n
			:param scale: POWer| VOLTage
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dpd')"""
		param = Conversions.enum_scalar_to_str(scale, enums.IqOutEnvScale)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:IQ:DPD{stream_cmd_val}:SCALe {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.IqOutEnvScale:
		"""SCPI: [SOURce<HW>]:IQ:DPD<ST>:SCALe \n
		Snippet: value: enums.IqOutEnvScale = driver.source.iq.dpd.scale.get(stream = repcap.Stream.Default) \n
		Determines the units used on the x and y-axis. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dpd')
			:return: scale: POWer| VOLTage"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:IQ:DPD{stream_cmd_val}:SCALe?')
		return Conversions.str_to_scalar_enum(response, enums.IqOutEnvScale)

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Model:
	"""Model commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("model", core, parent)

	def set(self, environment: enums.ObscEnvModel, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ENVironment:[MODel] \n
		Snippet: driver.source.bb.gnss.receiver.v.environment.model.set(environment = enums.ObscEnvModel.FULL, stream = repcap.Stream.Default) \n
		Sets the environment model. \n
			:param environment: LOS| MPATh
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')"""
		param = Conversions.enum_scalar_to_str(environment, enums.ObscEnvModel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:ENVironment:MODel {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.ObscEnvModel:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ENVironment:[MODel] \n
		Snippet: value: enums.ObscEnvModel = driver.source.bb.gnss.receiver.v.environment.model.get(stream = repcap.Stream.Default) \n
		Sets the environment model. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:return: environment: LOS| MPATh"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:ENVironment:MODel?')
		return Conversions.str_to_scalar_enum(response, enums.ObscEnvModel)

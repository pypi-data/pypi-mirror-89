from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Period:
	"""Period commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("period", core, parent)

	def set(self, interval: int, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SYSTem:SBAS:WAAS<ST>:NMESsage:NAV:SERVice:PERiod \n
		Snippet: driver.source.bb.gnss.system.sbas.waas.nmessage.nav.service.period.set(interval = 1, stream = repcap.Stream.Default) \n
		Sets the periodicity of the SBAS message. \n
			:param interval: integer Range: 0 to 999
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbas')"""
		param = Conversions.decimal_value_to_str(interval)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SYSTem:SBAS:WAAS{stream_cmd_val}:NMESsage:NAV:SERVice:PERiod {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SYSTem:SBAS:WAAS<ST>:NMESsage:NAV:SERVice:PERiod \n
		Snippet: value: int = driver.source.bb.gnss.system.sbas.waas.nmessage.nav.service.period.get(stream = repcap.Stream.Default) \n
		Sets the periodicity of the SBAS message. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbas')
			:return: interval: integer Range: 0 to 999"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SYSTem:SBAS:WAAS{stream_cmd_val}:NMESsage:NAV:SERVice:PERiod?')
		return Conversions.str_to_int(response)

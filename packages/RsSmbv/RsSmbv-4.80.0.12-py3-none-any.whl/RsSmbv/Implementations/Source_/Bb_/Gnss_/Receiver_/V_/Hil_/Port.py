from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Port:
	"""Port commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("port", core, parent)

	def set(self, udp_port: int, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:HIL:PORT \n
		Snippet: driver.source.bb.gnss.receiver.v.hil.port.set(udp_port = 1, stream = repcap.Stream.Default) \n
		Set the UDP port number at the R&S SMBV100B for the HIL interface. \n
			:param udp_port: integer Range: 0 to 65535
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')"""
		param = Conversions.decimal_value_to_str(udp_port)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:HIL:PORT {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:HIL:PORT \n
		Snippet: value: int = driver.source.bb.gnss.receiver.v.hil.port.get(stream = repcap.Stream.Default) \n
		Set the UDP port number at the R&S SMBV100B for the HIL interface. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:return: udp_port: integer Range: 0 to 65535"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:HIL:PORT?')
		return Conversions.str_to_int(response)

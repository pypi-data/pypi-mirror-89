from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ttiedch:
	"""Ttiedch commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ttiedch", core, parent)

	def set(self, ttiedch: enums.HsUpaDchTti, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:[HSUPa]:EDCH:TTIEdch \n
		Snippet: driver.source.bb.w3Gpp.mstation.hsupa.edch.ttiedch.set(ttiedch = enums.HsUpaDchTti._10ms, stream = repcap.Stream.Default) \n
		Sets the value for the TTI size (Transmission Time Interval) . This command is a query only, if an UL-DTX is enabled
		(method RsSmbv.Source.Bb.W3Gpp.Mstation.Udtx.state ON) or an FRC is activated (BB:W3GPp:DPCCh:E:FRC:STATe ON) . \n
			:param ttiedch: 2ms| 10ms
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.enum_scalar_to_str(ttiedch, enums.HsUpaDchTti)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:HSUPa:EDCH:TTIEdch {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.HsUpaDchTti:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:[HSUPa]:EDCH:TTIEdch \n
		Snippet: value: enums.HsUpaDchTti = driver.source.bb.w3Gpp.mstation.hsupa.edch.ttiedch.get(stream = repcap.Stream.Default) \n
		Sets the value for the TTI size (Transmission Time Interval) . This command is a query only, if an UL-DTX is enabled
		(method RsSmbv.Source.Bb.W3Gpp.Mstation.Udtx.state ON) or an FRC is activated (BB:W3GPp:DPCCh:E:FRC:STATe ON) . \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: ttiedch: 2ms| 10ms"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:HSUPa:EDCH:TTIEdch?')
		return Conversions.str_to_scalar_enum(response, enums.HsUpaDchTti)

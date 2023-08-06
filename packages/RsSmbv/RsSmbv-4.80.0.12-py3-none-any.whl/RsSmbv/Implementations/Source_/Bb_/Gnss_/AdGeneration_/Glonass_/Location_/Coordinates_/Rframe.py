from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rframe:
	"""Rframe commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rframe", core, parent)

	def set(self, reference_frame: enums.RefFrame, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GLONass<ST>:LOCation:COORdinates:RFRame \n
		Snippet: driver.source.bb.gnss.adGeneration.glonass.location.coordinates.rframe.set(reference_frame = enums.RefFrame.PZ90, stream = repcap.Stream.Default) \n
		Sets the reference frame. \n
			:param reference_frame: PZ90| WGS84
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Glonass')"""
		param = Conversions.enum_scalar_to_str(reference_frame, enums.RefFrame)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:GLONass{stream_cmd_val}:LOCation:COORdinates:RFRame {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.RefFrame:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GLONass<ST>:LOCation:COORdinates:RFRame \n
		Snippet: value: enums.RefFrame = driver.source.bb.gnss.adGeneration.glonass.location.coordinates.rframe.get(stream = repcap.Stream.Default) \n
		Sets the reference frame. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Glonass')
			:return: reference_frame: PZ90| WGS84"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:GLONass{stream_cmd_val}:LOCation:COORdinates:RFRame?')
		return Conversions.str_to_scalar_enum(response, enums.RefFrame)

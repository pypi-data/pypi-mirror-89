from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Time:
	"""Time commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("time", core, parent)

	def set(self, time: enums.FmStereoTimeCfgSel, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:STEReo:GRPS:GT<ST>:TIME \n
		Snippet: driver.source.bb.stereo.grps.gt.time.set(time = enums.FmStereoTimeCfgSel.SYSTime, stream = repcap.Stream.Default) \n
		No command help available \n
			:param time: No help available
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gt')"""
		param = Conversions.enum_scalar_to_str(time, enums.FmStereoTimeCfgSel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:GRPS:GT{stream_cmd_val}:TIME {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.FmStereoTimeCfgSel:
		"""SCPI: [SOURce<HW>]:BB:STEReo:GRPS:GT<ST>:TIME \n
		Snippet: value: enums.FmStereoTimeCfgSel = driver.source.bb.stereo.grps.gt.time.get(stream = repcap.Stream.Default) \n
		No command help available \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gt')
			:return: time: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:STEReo:GRPS:GT{stream_cmd_val}:TIME?')
		return Conversions.str_to_scalar_enum(response, enums.FmStereoTimeCfgSel)

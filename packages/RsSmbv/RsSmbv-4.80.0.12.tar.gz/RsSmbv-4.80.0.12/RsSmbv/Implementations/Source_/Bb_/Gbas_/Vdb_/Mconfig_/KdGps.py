from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class KdGps:
	"""KdGps commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("kdGps", core, parent)

	def set(self, kmd_ed_gps: float, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:KDGPs \n
		Snippet: driver.source.bb.gbas.vdb.mconfig.kdGps.set(kmd_ed_gps = 1.0, channel = repcap.Channel.Default) \n
		Sets the ephemeris missed detection parameter (Kmd_e) , GAST D. This is a multiplier considered when calculating the
		ephemeris error position bound for GAST D. It is derived from the probability that a detection is missed because of an
		ephemeris error in a GPS/GLONASS satellite. \n
			:param kmd_ed_gps: float Range: 0 to 12.75
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')"""
		param = Conversions.decimal_value_to_str(kmd_ed_gps)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:KDGPs {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:KDGPs \n
		Snippet: value: float = driver.source.bb.gbas.vdb.mconfig.kdGps.get(channel = repcap.Channel.Default) \n
		Sets the ephemeris missed detection parameter (Kmd_e) , GAST D. This is a multiplier considered when calculating the
		ephemeris error position bound for GAST D. It is derived from the probability that a detection is missed because of an
		ephemeris error in a GPS/GLONASS satellite. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:return: kmd_ed_gps: float Range: 0 to 12.75"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:KDGPs?')
		return Conversions.str_to_float(response)

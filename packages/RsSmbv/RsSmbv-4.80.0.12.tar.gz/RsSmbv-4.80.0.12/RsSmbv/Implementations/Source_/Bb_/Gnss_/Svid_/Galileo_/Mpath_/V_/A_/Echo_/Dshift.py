from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dshift:
	"""Dshift commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dshift", core, parent)

	def set(self, doppler_shift: float, channel=repcap.Channel.Default, stream=repcap.Stream.Default, vehicle=repcap.Vehicle.Default, antenna=repcap.Antenna.Default, echoes=repcap.Echoes.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GALileo<ST>:MPATh:[V<US>]:[A<GR>]:ECHO<S2US>:DSHift \n
		Snippet: driver.source.bb.gnss.svid.galileo.mpath.v.a.echo.dshift.set(doppler_shift = 1.0, channel = repcap.Channel.Default, stream = repcap.Stream.Default, vehicle = repcap.Vehicle.Default, antenna = repcap.Antenna.Default, echoes = repcap.Echoes.Default) \n
		Sets an additional Doppler shift. \n
			:param doppler_shift: float Range: -10E3 to 10E3, Unit: Hz
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Galileo')
			:param vehicle: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:param antenna: optional repeated capability selector. Default value: Nr1 (settable in the interface 'A')
			:param echoes: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Echo')"""
		param = Conversions.decimal_value_to_str(doppler_shift)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		vehicle_cmd_val = self._base.get_repcap_cmd_value(vehicle, repcap.Vehicle)
		antenna_cmd_val = self._base.get_repcap_cmd_value(antenna, repcap.Antenna)
		echoes_cmd_val = self._base.get_repcap_cmd_value(echoes, repcap.Echoes)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GALileo{stream_cmd_val}:MPATh:V{vehicle_cmd_val}:A{antenna_cmd_val}:ECHO{echoes_cmd_val}:DSHift {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, vehicle=repcap.Vehicle.Default, antenna=repcap.Antenna.Default, echoes=repcap.Echoes.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GALileo<ST>:MPATh:[V<US>]:[A<GR>]:ECHO<S2US>:DSHift \n
		Snippet: value: float = driver.source.bb.gnss.svid.galileo.mpath.v.a.echo.dshift.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default, vehicle = repcap.Vehicle.Default, antenna = repcap.Antenna.Default, echoes = repcap.Echoes.Default) \n
		Sets an additional Doppler shift. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Galileo')
			:param vehicle: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:param antenna: optional repeated capability selector. Default value: Nr1 (settable in the interface 'A')
			:param echoes: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Echo')
			:return: doppler_shift: float Range: -10E3 to 10E3, Unit: Hz"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		vehicle_cmd_val = self._base.get_repcap_cmd_value(vehicle, repcap.Vehicle)
		antenna_cmd_val = self._base.get_repcap_cmd_value(antenna, repcap.Antenna)
		echoes_cmd_val = self._base.get_repcap_cmd_value(echoes, repcap.Echoes)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GALileo{stream_cmd_val}:MPATh:V{vehicle_cmd_val}:A{antenna_cmd_val}:ECHO{echoes_cmd_val}:DSHift?')
		return Conversions.str_to_float(response)

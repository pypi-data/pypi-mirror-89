from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Azero:
	"""Azero commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("azero", core, parent)

	@property
	def unscaled(self):
		"""unscaled commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_unscaled'):
			from .Azero_.Unscaled import Unscaled
			self._unscaled = Unscaled(self._core, self._base)
		return self._unscaled

	def set(self, azero: int, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TIME:CONVersion:SBAS<ST>:GAGAN:UTC:AZERo \n
		Snippet: driver.source.bb.gnss.time.conversion.sbas.gagan.utc.azero.set(azero = 1, stream = repcap.Stream.Default) \n
		Sets the constant term of polynomial, A0. \n
			:param azero: integer Range: -2147483648 to 2147483647
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbas')"""
		param = Conversions.decimal_value_to_str(azero)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:TIME:CONVersion:SBAS{stream_cmd_val}:GAGAN:UTC:AZERo {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TIME:CONVersion:SBAS<ST>:GAGAN:UTC:AZERo \n
		Snippet: value: int = driver.source.bb.gnss.time.conversion.sbas.gagan.utc.azero.get(stream = repcap.Stream.Default) \n
		Sets the constant term of polynomial, A0. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbas')
			:return: azero: integer Range: -2147483648 to 2147483647"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:TIME:CONVersion:SBAS{stream_cmd_val}:GAGAN:UTC:AZERo?')
		return Conversions.str_to_int(response)

	def clone(self) -> 'Azero':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Azero(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Aone:
	"""Aone commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("aone", core, parent)

	@property
	def unscaled(self):
		"""unscaled commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_unscaled'):
			from .Aone_.Unscaled import Unscaled
			self._unscaled = Unscaled(self._core, self._base)
		return self._unscaled

	def set(self, aone: int, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TIME:CONVersion:SBAS<ST>:GAGAN:UTC:AONE \n
		Snippet: driver.source.bb.gnss.time.conversion.sbas.gagan.utc.aone.set(aone = 1, stream = repcap.Stream.Default) \n
		Sets the first order term of polynomial, A1. \n
			:param aone: integer Range: -8388608 to 8388607
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbas')"""
		param = Conversions.decimal_value_to_str(aone)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:TIME:CONVersion:SBAS{stream_cmd_val}:GAGAN:UTC:AONE {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TIME:CONVersion:SBAS<ST>:GAGAN:UTC:AONE \n
		Snippet: value: int = driver.source.bb.gnss.time.conversion.sbas.gagan.utc.aone.get(stream = repcap.Stream.Default) \n
		Sets the first order term of polynomial, A1. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbas')
			:return: aone: integer Range: -8388608 to 8388607"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:TIME:CONVersion:SBAS{stream_cmd_val}:GAGAN:UTC:AONE?')
		return Conversions.str_to_int(response)

	def clone(self) -> 'Aone':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Aone(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

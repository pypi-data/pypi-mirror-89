from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Data:
	"""Data commands group definition. 3 total commands, 2 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("data", core, parent)

	@property
	def dselect(self):
		"""dselect commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dselect'):
			from .Data_.Dselect import Dselect
			self._dselect = Dselect(self._core, self._base)
		return self._dselect

	@property
	def pattern(self):
		"""pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .Data_.Pattern import Pattern
			self._pattern = Pattern(self._core, self._base)
		return self._pattern

	def set(self, data: enums.TpcDataSour, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:C2K:MSTation<ST>:TPC:DATA \n
		Snippet: driver.source.bb.c2K.mstation.tpc.data.set(data = enums.TpcDataSour.DLISt, stream = repcap.Stream.Default) \n
		Sets the data source for the power control bits of the traffic channels. \n
			:param data: ZERO| ONE| PATTern| DLISt DLISt A data list is used. The data list is selected with the command method RsSmbv.Source.Bb.C2K.Mstation.Tpc.Data.Dselect.set. ZERO | ONE Internal 0 and 1 data is used. PATTern Internal data is used. The bit pattern for the data is defined by the command method RsSmbv.Source.Bb.C2K.Mstation.Tpc.Data.Pattern.set. The maximum length is 64 bits.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.enum_scalar_to_str(data, enums.TpcDataSour)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:MSTation{stream_cmd_val}:TPC:DATA {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.TpcDataSour:
		"""SCPI: [SOURce<HW>]:BB:C2K:MSTation<ST>:TPC:DATA \n
		Snippet: value: enums.TpcDataSour = driver.source.bb.c2K.mstation.tpc.data.get(stream = repcap.Stream.Default) \n
		Sets the data source for the power control bits of the traffic channels. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: data: ZERO| ONE| PATTern| DLISt DLISt A data list is used. The data list is selected with the command method RsSmbv.Source.Bb.C2K.Mstation.Tpc.Data.Dselect.set. ZERO | ONE Internal 0 and 1 data is used. PATTern Internal data is used. The bit pattern for the data is defined by the command method RsSmbv.Source.Bb.C2K.Mstation.Tpc.Data.Pattern.set. The maximum length is 64 bits."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:C2K:MSTation{stream_cmd_val}:TPC:DATA?')
		return Conversions.str_to_scalar_enum(response, enums.TpcDataSour)

	def clone(self) -> 'Data':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Data(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Data:
	"""Data commands group definition. 3 total commands, 2 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("data", core, parent)

	@property
	def dselection(self):
		"""dselection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dselection'):
			from .Data_.Dselection import Dselection
			self._dselection = Dselection(self._core, self._base)
		return self._dselection

	@property
	def pattern(self):
		"""pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .Data_.Pattern import Pattern
			self._pattern = Pattern(self._core, self._base)
		return self._pattern

	def set(self, data: enums.GbasDataSource, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:DATA \n
		Snippet: driver.source.bb.gbas.vdb.data.set(data = enums.GbasDataSource.DLISt, channel = repcap.Channel.Default) \n
		Selects the data source, e.g. a sequence of 0 or 1, a pseudo-random sequence with different length, a pattern or a data
		list (DLISt) . \n
			:param data: ZERO| ONE| PATTern| PN9| PN11| PN15| PN16| PN20| PN21| PN23| DLISt| RGData
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')"""
		param = Conversions.enum_scalar_to_str(data, enums.GbasDataSource)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:DATA {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.GbasDataSource:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:DATA \n
		Snippet: value: enums.GbasDataSource = driver.source.bb.gbas.vdb.data.get(channel = repcap.Channel.Default) \n
		Selects the data source, e.g. a sequence of 0 or 1, a pseudo-random sequence with different length, a pattern or a data
		list (DLISt) . \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:return: data: ZERO| ONE| PATTern| PN9| PN11| PN15| PN16| PN20| PN21| PN23| DLISt| RGData"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:DATA?')
		return Conversions.str_to_scalar_enum(response, enums.GbasDataSource)

	def clone(self) -> 'Data':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Data(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

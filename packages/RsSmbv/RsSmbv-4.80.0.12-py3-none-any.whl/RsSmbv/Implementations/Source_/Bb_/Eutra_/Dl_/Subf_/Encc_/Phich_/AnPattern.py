from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.Utilities import trim_str_response
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AnPattern:
	"""AnPattern commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: Group, default value after init: Group.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("anPattern", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_group_get', 'repcap_group_set', repcap.Group.Nr1)

	def repcap_group_set(self, enum_value: repcap.Group) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Group.Default
		Default value after init: Group.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_group_get(self) -> repcap.Group:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def set(self, an_pattern: str, stream=repcap.Stream.Default, group=repcap.Group.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PHICh:ANPattern<GR> \n
		Snippet: driver.source.bb.eutra.dl.subf.encc.phich.anPattern.set(an_pattern = '1', stream = repcap.Stream.Default, group = repcap.Group.Default) \n
		No command help available \n
			:param an_pattern: No help available
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param group: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AnPattern')"""
		param = Conversions.value_to_quoted_str(an_pattern)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		group_cmd_val = self._base.get_repcap_cmd_value(group, repcap.Group)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PHICh:ANPattern{group_cmd_val} {param}')

	def get(self, stream=repcap.Stream.Default, group=repcap.Group.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PHICh:ANPattern<GR> \n
		Snippet: value: str = driver.source.bb.eutra.dl.subf.encc.phich.anPattern.get(stream = repcap.Stream.Default, group = repcap.Group.Default) \n
		No command help available \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param group: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AnPattern')
			:return: an_pattern: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		group_cmd_val = self._base.get_repcap_cmd_value(group, repcap.Group)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PHICh:ANPattern{group_cmd_val}?')
		return trim_str_response(response)

	def clone(self) -> 'AnPattern':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AnPattern(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

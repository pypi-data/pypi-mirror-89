from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Subframe:
	"""Subframe commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: SubframeIx, default value after init: SubframeIx.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("subframe", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_subframeIx_get', 'repcap_subframeIx_set', repcap.SubframeIx.Nr1)

	def repcap_subframeIx_set(self, enum_value: repcap.SubframeIx) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to SubframeIx.Default
		Default value after init: SubframeIx.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_subframeIx_get(self) -> repcap.SubframeIx:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def set(self, valid_sub_frames: bool, subframeIx=repcap.SubframeIx.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:EMTC:VALid:SUBFrame<DIR> \n
		Snippet: driver.source.bb.eutra.ul.emtc.valid.subframe.set(valid_sub_frames = False, subframeIx = repcap.SubframeIx.Default) \n
		Sets a subframe as valid and used for eMTC transmission. \n
			:param valid_sub_frames: 0| 1| OFF| ON
			:param subframeIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subframe')"""
		param = Conversions.bool_to_str(valid_sub_frames)
		subframeIx_cmd_val = self._base.get_repcap_cmd_value(subframeIx, repcap.SubframeIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:EMTC:VALid:SUBFrame{subframeIx_cmd_val} {param}')

	def get(self, subframeIx=repcap.SubframeIx.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:EMTC:VALid:SUBFrame<DIR> \n
		Snippet: value: bool = driver.source.bb.eutra.ul.emtc.valid.subframe.get(subframeIx = repcap.SubframeIx.Default) \n
		Sets a subframe as valid and used for eMTC transmission. \n
			:param subframeIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subframe')
			:return: valid_sub_frames: 0| 1| OFF| ON"""
		subframeIx_cmd_val = self._base.get_repcap_cmd_value(subframeIx, repcap.SubframeIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:EMTC:VALid:SUBFrame{subframeIx_cmd_val}?')
		return Conversions.str_to_bool(response)

	def clone(self) -> 'Subframe':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Subframe(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

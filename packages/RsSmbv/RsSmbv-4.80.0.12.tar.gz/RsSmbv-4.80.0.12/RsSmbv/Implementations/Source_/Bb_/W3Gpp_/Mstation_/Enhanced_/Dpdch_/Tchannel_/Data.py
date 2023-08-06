from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


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

	def set(self, data: enums.DataSour, transportChannel=repcap.TransportChannel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation:ENHanced:DPDCh:TCHannel<DI>:DATA \n
		Snippet: driver.source.bb.w3Gpp.mstation.enhanced.dpdch.tchannel.data.set(data = enums.DataSour.DLISt, transportChannel = repcap.TransportChannel.Default) \n
		Selects the data source for the transport channel. \n
			:param data: ZERO| ONE| PATTern| PN9| PN11| PN15| PN16| PN20| PN21| PN23| DLISt PNxx The pseudo-random sequence generator is used as the data source. Different random sequence lengths can be selected. DLISt A data list is used. The data list is selected with the command method RsSmbv.Source.Bb.W3Gpp.Mstation.Enhanced.Dpdch.Tchannel.Data.Dselect.set. ZERO | ONE Internal 0 and 1 data is used. PATTern Internal data is used. The bit pattern for the data is defined by the command method RsSmbv.Source.Bb.W3Gpp.Mstation.Enhanced.Dpdch.Tchannel.Data.Pattern.set.
			:param transportChannel: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tchannel')"""
		param = Conversions.enum_scalar_to_str(data, enums.DataSour)
		transportChannel_cmd_val = self._base.get_repcap_cmd_value(transportChannel, repcap.TransportChannel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:TCHannel{transportChannel_cmd_val}:DATA {param}')

	# noinspection PyTypeChecker
	def get(self, transportChannel=repcap.TransportChannel.Default) -> enums.DataSour:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation:ENHanced:DPDCh:TCHannel<DI>:DATA \n
		Snippet: value: enums.DataSour = driver.source.bb.w3Gpp.mstation.enhanced.dpdch.tchannel.data.get(transportChannel = repcap.TransportChannel.Default) \n
		Selects the data source for the transport channel. \n
			:param transportChannel: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tchannel')
			:return: data: ZERO| ONE| PATTern| PN9| PN11| PN15| PN16| PN20| PN21| PN23| DLISt PNxx The pseudo-random sequence generator is used as the data source. Different random sequence lengths can be selected. DLISt A data list is used. The data list is selected with the command method RsSmbv.Source.Bb.W3Gpp.Mstation.Enhanced.Dpdch.Tchannel.Data.Dselect.set. ZERO | ONE Internal 0 and 1 data is used. PATTern Internal data is used. The bit pattern for the data is defined by the command method RsSmbv.Source.Bb.W3Gpp.Mstation.Enhanced.Dpdch.Tchannel.Data.Pattern.set."""
		transportChannel_cmd_val = self._base.get_repcap_cmd_value(transportChannel, repcap.TransportChannel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:TCHannel{transportChannel_cmd_val}:DATA?')
		return Conversions.str_to_scalar_enum(response, enums.DataSour)

	def clone(self) -> 'Data':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Data(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

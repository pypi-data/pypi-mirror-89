from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal import Conversions
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nresources:
	"""Nresources commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nresources", core, parent)

	def set(self, resources: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default, srsRsrcSet=repcap.SrsRsrcSet.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:DL:BWP<DIR>:CSIRs:NZP:SET<GR>:NRESources \n
		Snippet: driver.source.bb.nr5G.ubwp.user.cell.dl.bwp.csirs.nzp.set.nresources.set(resources = 1, channel = repcap.Channel.Default, stream = repcap.Stream.Default, numSuffix = repcap.NumSuffix.Default, srsRsrcSet = repcap.SrsRsrcSet.Default) \n
		Sets the number of CSI-RS resources. \n
			:param resources: integer Range: 0 to 64
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param srsRsrcSet: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Set')"""
		param = Conversions.decimal_value_to_str(resources)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		srsRsrcSet_cmd_val = self._base.get_repcap_cmd_value(srsRsrcSet, repcap.SrsRsrcSet)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:DL:BWP{numSuffix_cmd_val}:CSIRs:NZP:SET{srsRsrcSet_cmd_val}:NRESources {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default, srsRsrcSet=repcap.SrsRsrcSet.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:DL:BWP<DIR>:CSIRs:NZP:SET<GR>:NRESources \n
		Snippet: value: int = driver.source.bb.nr5G.ubwp.user.cell.dl.bwp.csirs.nzp.set.nresources.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default, numSuffix = repcap.NumSuffix.Default, srsRsrcSet = repcap.SrsRsrcSet.Default) \n
		Sets the number of CSI-RS resources. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param srsRsrcSet: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Set')
			:return: resources: integer Range: 0 to 64"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		srsRsrcSet_cmd_val = self._base.get_repcap_cmd_value(srsRsrcSet, repcap.SrsRsrcSet)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:DL:BWP{numSuffix_cmd_val}:CSIRs:NZP:SET{srsRsrcSet_cmd_val}:NRESources?')
		return Conversions.str_to_int(response)

from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Knull:
	"""Knull commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("knull", core, parent)

	def set(self, k_0: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default, pdschTdoAlloc=repcap.PdschTdoAlloc.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:DL:BWP<DIR>:PDSCh:TD<GRP>:KNULl \n
		Snippet: driver.source.bb.nr5G.ubwp.user.cell.dl.bwp.pdsch.td.knull.set(k_0 = 1, channel = repcap.Channel.Default, stream = repcap.Stream.Default, numSuffix = repcap.NumSuffix.Default, pdschTdoAlloc = repcap.PdschTdoAlloc.Default) \n
		Sets the slot offset K0. \n
			:param k_0: integer Range: 0 to 32
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param pdschTdoAlloc: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Td')"""
		param = Conversions.decimal_value_to_str(k_0)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		pdschTdoAlloc_cmd_val = self._base.get_repcap_cmd_value(pdschTdoAlloc, repcap.PdschTdoAlloc)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:DL:BWP{numSuffix_cmd_val}:PDSCh:TD{pdschTdoAlloc_cmd_val}:KNULl {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default, pdschTdoAlloc=repcap.PdschTdoAlloc.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:DL:BWP<DIR>:PDSCh:TD<GRP>:KNULl \n
		Snippet: value: int = driver.source.bb.nr5G.ubwp.user.cell.dl.bwp.pdsch.td.knull.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default, numSuffix = repcap.NumSuffix.Default, pdschTdoAlloc = repcap.PdschTdoAlloc.Default) \n
		Sets the slot offset K0. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param pdschTdoAlloc: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Td')
			:return: k_0: integer Range: 0 to 32"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		pdschTdoAlloc_cmd_val = self._base.get_repcap_cmd_value(pdschTdoAlloc, repcap.PdschTdoAlloc)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:DL:BWP{numSuffix_cmd_val}:PDSCh:TD{pdschTdoAlloc_cmd_val}:KNULl?')
		return Conversions.str_to_int(response)

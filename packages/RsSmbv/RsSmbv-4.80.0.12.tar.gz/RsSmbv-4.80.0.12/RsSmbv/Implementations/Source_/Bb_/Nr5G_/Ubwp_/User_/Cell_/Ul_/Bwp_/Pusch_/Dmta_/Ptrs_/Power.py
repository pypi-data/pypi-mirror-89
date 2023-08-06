from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal import Conversions
from ............. import enums
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("power", core, parent)

	def set(self, ptrs_power: enums.PtrsPower, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:UL:BWP<DIR>:PUSCh:DMTA:PTRS:POWer \n
		Snippet: driver.source.bb.nr5G.ubwp.user.cell.ul.bwp.pusch.dmta.ptrs.power.set(ptrs_power = enums.PtrsPower.P00, channel = repcap.Channel.Default, stream = repcap.Stream.Default, numSuffix = repcap.NumSuffix.Default) \n
		Sets the parameter ptrs-Power and thus defines the PUSCH to PTRS power ratio per layer per resource element. \n
			:param ptrs_power: P00| P01
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')"""
		param = Conversions.enum_scalar_to_str(ptrs_power, enums.PtrsPower)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:UL:BWP{numSuffix_cmd_val}:PUSCh:DMTA:PTRS:POWer {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default) -> enums.PtrsPower:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:UL:BWP<DIR>:PUSCh:DMTA:PTRS:POWer \n
		Snippet: value: enums.PtrsPower = driver.source.bb.nr5G.ubwp.user.cell.ul.bwp.pusch.dmta.ptrs.power.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default, numSuffix = repcap.NumSuffix.Default) \n
		Sets the parameter ptrs-Power and thus defines the PUSCH to PTRS power ratio per layer per resource element. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:return: ptrs_power: P00| P01"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:UL:BWP{numSuffix_cmd_val}:PUSCh:DMTA:PTRS:POWer?')
		return Conversions.str_to_scalar_enum(response, enums.PtrsPower)

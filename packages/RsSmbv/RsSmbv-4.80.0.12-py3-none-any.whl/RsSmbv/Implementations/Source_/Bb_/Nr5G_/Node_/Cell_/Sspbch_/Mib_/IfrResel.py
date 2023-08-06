from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IfrResel:
	"""IfrResel commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ifrResel", core, parent)

	def set(self, ssp_bch_in_freq_sel: enums.FreqSel, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:SSPBch<ST>:MIB:IFRResel \n
		Snippet: driver.source.bb.nr5G.node.cell.sspbch.mib.ifrResel.set(ssp_bch_in_freq_sel = enums.FreqSel.ALWD, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the value of the system information parameter intraFreqReselection. \n
			:param ssp_bch_in_freq_sel: ALWD| NALW
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sspbch')"""
		param = Conversions.enum_scalar_to_str(ssp_bch_in_freq_sel, enums.FreqSel)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:SSPBch{stream_cmd_val}:MIB:IFRResel {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.FreqSel:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:SSPBch<ST>:MIB:IFRResel \n
		Snippet: value: enums.FreqSel = driver.source.bb.nr5G.node.cell.sspbch.mib.ifrResel.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the value of the system information parameter intraFreqReselection. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sspbch')
			:return: ssp_bch_in_freq_sel: ALWD| NALW"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:SSPBch{stream_cmd_val}:MIB:IFRResel?')
		return Conversions.str_to_scalar_enum(response, enums.FreqSel)

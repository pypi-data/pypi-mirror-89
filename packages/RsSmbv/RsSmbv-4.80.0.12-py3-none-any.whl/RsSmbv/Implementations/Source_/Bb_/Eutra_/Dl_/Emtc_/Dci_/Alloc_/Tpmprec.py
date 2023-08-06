from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tpmprec:
	"""Tpmprec commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tpmprec", core, parent)

	def set(self, dci_tpmi_prec: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:EMTC:DCI:ALLoc<CH>:TPMPrec \n
		Snippet: driver.source.bb.eutra.dl.emtc.dci.alloc.tpmprec.set(dci_tpmi_prec = 1, channel = repcap.Channel.Default) \n
		Sets the DCI field TPMI information for precoding. \n
			:param dci_tpmi_prec: integer Range: 0 to 15
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')"""
		param = Conversions.decimal_value_to_str(dci_tpmi_prec)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:DCI:ALLoc{channel_cmd_val}:TPMPrec {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:EMTC:DCI:ALLoc<CH>:TPMPrec \n
		Snippet: value: int = driver.source.bb.eutra.dl.emtc.dci.alloc.tpmprec.get(channel = repcap.Channel.Default) \n
		Sets the DCI field TPMI information for precoding. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: dci_tpmi_prec: integer Range: 0 to 15"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:DCI:ALLoc{channel_cmd_val}:TPMPrec?')
		return Conversions.str_to_int(response)

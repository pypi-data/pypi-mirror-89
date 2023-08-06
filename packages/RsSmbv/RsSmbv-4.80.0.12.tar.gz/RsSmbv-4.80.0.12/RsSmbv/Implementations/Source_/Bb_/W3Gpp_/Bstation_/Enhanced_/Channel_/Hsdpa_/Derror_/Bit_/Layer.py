from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import enums
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Layer:
	"""Layer commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("layer", core, parent)

	def set(self, layer: enums.EnhBitErr, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation:[ENHanced]:CHANnel<CH>:HSDPa:DERRor:BIT:LAYer \n
		Snippet: driver.source.bb.w3Gpp.bstation.enhanced.channel.hsdpa.derror.bit.layer.set(layer = enums.EnhBitErr.PHYSical, channel = repcap.Channel.Default) \n
		The command selects the layer in the coding process in which bit errors are inserted. \n
			:param layer: TRANsport| PHYSical TRANsport Transport Layer (Layer 2) PHYSical Physical layer (Layer 1)
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.enum_scalar_to_str(layer, enums.EnhBitErr)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation:ENHanced:CHANnel{channel_cmd_val}:HSDPa:DERRor:BIT:LAYer {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EnhBitErr:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation:[ENHanced]:CHANnel<CH>:HSDPa:DERRor:BIT:LAYer \n
		Snippet: value: enums.EnhBitErr = driver.source.bb.w3Gpp.bstation.enhanced.channel.hsdpa.derror.bit.layer.get(channel = repcap.Channel.Default) \n
		The command selects the layer in the coding process in which bit errors are inserted. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: layer: TRANsport| PHYSical TRANsport Transport Layer (Layer 2) PHYSical Physical layer (Layer 1)"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation:ENHanced:CHANnel{channel_cmd_val}:HSDPa:DERRor:BIT:LAYer?')
		return Conversions.str_to_scalar_enum(response, enums.EnhBitErr)

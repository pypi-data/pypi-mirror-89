from ..............Internal.Core import Core
from ..............Internal.CommandsGroup import CommandsGroup
from ..............Internal import Conversions
from .............. import enums
from .............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ports:
	"""Ports commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ports", core, parent)

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default, srsRsrcSet=repcap.SrsRsrcSet.Default, srsRsrcSetRsrc=repcap.SrsRsrcSetRsrc.Default) -> enums.AllPorts:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:DL:BWP<DIR>:CSIRs:NZP:SET<GR>:RES<USER>:PORTs \n
		Snippet: value: enums.AllPorts = driver.source.bb.nr5G.ubwp.user.cell.dl.bwp.csirs.nzp.set.res.ports.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default, numSuffix = repcap.NumSuffix.Default, srsRsrcSet = repcap.SrsRsrcSet.Default, srsRsrcSetRsrc = repcap.SrsRsrcSetRsrc.Default) \n
		Sets the number of ports X. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param srsRsrcSet: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Set')
			:param srsRsrcSetRsrc: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Res')
			:return: ports: 1| 2| 4| 8| 12| 16| 24| 32"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		srsRsrcSet_cmd_val = self._base.get_repcap_cmd_value(srsRsrcSet, repcap.SrsRsrcSet)
		srsRsrcSetRsrc_cmd_val = self._base.get_repcap_cmd_value(srsRsrcSetRsrc, repcap.SrsRsrcSetRsrc)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:DL:BWP{numSuffix_cmd_val}:CSIRs:NZP:SET{srsRsrcSet_cmd_val}:RES{srsRsrcSetRsrc_cmd_val}:PORTs?')
		return Conversions.str_to_scalar_enum(response, enums.AllPorts)

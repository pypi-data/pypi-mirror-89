from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import enums
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Eprotection:
	"""Eprotection commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("eprotection", core, parent)

	def set(self, eprotection: enums.EnhTchErr, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:UP:CELL<ST>:ENH:DCH:DCCH<CH>:EPRotection \n
		Snippet: driver.source.bb.tdscdma.up.cell.enh.dch.dcch.eprotection.set(eprotection = enums.EnhTchErr.CON2, stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the error protection. \n
			:param eprotection: NONE| TURBo3| CON2| CON3
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dcch')"""
		param = Conversions.enum_scalar_to_str(eprotection, enums.EnhTchErr)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:UP:CELL{stream_cmd_val}:ENH:DCH:DCCH{channel_cmd_val}:EPRotection {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> enums.EnhTchErr:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:UP:CELL<ST>:ENH:DCH:DCCH<CH>:EPRotection \n
		Snippet: value: enums.EnhTchErr = driver.source.bb.tdscdma.up.cell.enh.dch.dcch.eprotection.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the error protection. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dcch')
			:return: eprotection: NONE| TURBo3| CON2| CON3"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:UP:CELL{stream_cmd_val}:ENH:DCH:DCCH{channel_cmd_val}:EPRotection?')
		return Conversions.str_to_scalar_enum(response, enums.EnhTchErr)

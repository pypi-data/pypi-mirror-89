from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Phase:
	"""Phase commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("phase", core, parent)

	def set(self, ssp_bch_app_hase: float, channel=repcap.Channel.Default, stream=repcap.Stream.Default, antennaPortMap=repcap.AntennaPortMap.Default, column=repcap.Column.Default, row=repcap.Row.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:SSPBch<ST>:POSition:APMap<DIR>:COL<GR>:ROW<USER>:PHASe \n
		Snippet: driver.source.bb.nr5G.node.cell.sspbch.position.apMap.col.row.phase.set(ssp_bch_app_hase = 1.0, channel = repcap.Channel.Default, stream = repcap.Stream.Default, antennaPortMap = repcap.AntennaPortMap.Default, column = repcap.Column.Default, row = repcap.Row.Default) \n
		Defines the mapping of the antenna ports to the physical antennas for the SS/PBCH pattern if cylindrical mapping
		coordinates are used. \n
			:param ssp_bch_app_hase: float Range: 0 to 360
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sspbch')
			:param antennaPortMap: optional repeated capability selector. Default value: Nr0 (settable in the interface 'ApMap')
			:param column: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Col')
			:param row: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Row')"""
		param = Conversions.decimal_value_to_str(ssp_bch_app_hase)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		antennaPortMap_cmd_val = self._base.get_repcap_cmd_value(antennaPortMap, repcap.AntennaPortMap)
		column_cmd_val = self._base.get_repcap_cmd_value(column, repcap.Column)
		row_cmd_val = self._base.get_repcap_cmd_value(row, repcap.Row)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:SSPBch{stream_cmd_val}:POSition:APMap{antennaPortMap_cmd_val}:COL{column_cmd_val}:ROW{row_cmd_val}:PHASe {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, antennaPortMap=repcap.AntennaPortMap.Default, column=repcap.Column.Default, row=repcap.Row.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:SSPBch<ST>:POSition:APMap<DIR>:COL<GR>:ROW<USER>:PHASe \n
		Snippet: value: float = driver.source.bb.nr5G.node.cell.sspbch.position.apMap.col.row.phase.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default, antennaPortMap = repcap.AntennaPortMap.Default, column = repcap.Column.Default, row = repcap.Row.Default) \n
		Defines the mapping of the antenna ports to the physical antennas for the SS/PBCH pattern if cylindrical mapping
		coordinates are used. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sspbch')
			:param antennaPortMap: optional repeated capability selector. Default value: Nr0 (settable in the interface 'ApMap')
			:param column: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Col')
			:param row: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Row')
			:return: ssp_bch_app_hase: float Range: 0 to 360"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		antennaPortMap_cmd_val = self._base.get_repcap_cmd_value(antennaPortMap, repcap.AntennaPortMap)
		column_cmd_val = self._base.get_repcap_cmd_value(column, repcap.Column)
		row_cmd_val = self._base.get_repcap_cmd_value(row, repcap.Row)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:SSPBch{stream_cmd_val}:POSition:APMap{antennaPortMap_cmd_val}:COL{column_cmd_val}:ROW{row_cmd_val}:PHASe?')
		return Conversions.str_to_float(response)

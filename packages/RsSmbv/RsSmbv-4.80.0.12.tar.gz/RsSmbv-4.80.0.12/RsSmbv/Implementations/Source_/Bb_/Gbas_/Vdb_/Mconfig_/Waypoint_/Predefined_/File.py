from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class File:
	"""File commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("file", core, parent)

	def set(self, wp_file: str, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:WAYPoint:PREDefined:FILE \n
		Snippet: driver.source.bb.gbas.vdb.mconfig.waypoint.predefined.file.set(wp_file = '1', channel = repcap.Channel.Default) \n
		Requires 'Mode > GBAS' (LAAS) header information. Loads the selected predefined file (extension *.txt) . \n
			:param wp_file: string Only the file name is required
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')"""
		param = Conversions.value_to_quoted_str(wp_file)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:WAYPoint:PREDefined:FILE {param}')

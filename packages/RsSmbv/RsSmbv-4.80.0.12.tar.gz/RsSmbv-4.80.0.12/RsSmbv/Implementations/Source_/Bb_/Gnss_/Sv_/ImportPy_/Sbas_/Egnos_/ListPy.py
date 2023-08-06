from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ListPy:
	"""ListPy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("listPy", core, parent)

	def get(self, stream=repcap.Stream.Default) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SV:IMPort:SBAS:EGNOS<ST>:LIST \n
		Snippet: value: List[str] = driver.source.bb.gnss.sv.importPy.sbas.egnos.listPy.get(stream = repcap.Stream.Default) \n
		Queries all *.ems files for EGNOS correction data *.nstb files for WAAS correction data of the import file list in a
		comma separated list. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbas')
			:return: gnss_dcw_in_files: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SV:IMPort:SBAS:EGNOS{stream_cmd_val}:LIST?')
		return Conversions.str_to_str_list(response)

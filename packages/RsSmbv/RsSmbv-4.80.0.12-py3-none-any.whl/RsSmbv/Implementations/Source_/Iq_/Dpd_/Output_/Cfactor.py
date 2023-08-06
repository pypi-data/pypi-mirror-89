from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cfactor:
	"""Cfactor commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cfactor", core, parent)

	def get(self, stream=repcap.Stream.Default) -> float:
		"""SCPI: [SOURce<HW>]:IQ:DPD<ST>:OUTPut:CFACtor \n
		Snippet: value: float = driver.source.iq.dpd.output.cfactor.get(stream = repcap.Stream.Default) \n
		Queries the measured values the before and after the enabled digital predistortion. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dpd')
			:return: crest_factor: float The query returns -1000 if the calculation is impossible or there are no measurements results available."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:IQ:DPD{stream_cmd_val}:OUTPut:CFACtor?')
		return Conversions.str_to_float(response)

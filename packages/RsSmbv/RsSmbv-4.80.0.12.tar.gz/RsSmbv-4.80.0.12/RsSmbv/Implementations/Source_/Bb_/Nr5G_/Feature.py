from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Feature:
	"""Feature commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("feature", core, parent)

	def get_activate(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:NR5G:FEATure:ACTivate \n
		Snippet: value: str = driver.source.bb.nr5G.feature.get_activate() \n
		No command help available \n
			:return: activat_hidden_fn: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:FEATure:ACTivate?')
		return trim_str_response(response)

	def set_activate(self, activat_hidden_fn: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:FEATure:ACTivate \n
		Snippet: driver.source.bb.nr5G.feature.set_activate(activat_hidden_fn = '1') \n
		No command help available \n
			:param activat_hidden_fn: No help available
		"""
		param = Conversions.value_to_quoted_str(activat_hidden_fn)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:FEATure:ACTivate {param}')

	def get_deactivate(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:NR5G:FEATure:DEACtivate \n
		Snippet: value: str = driver.source.bb.nr5G.feature.get_deactivate() \n
		No command help available \n
			:return: deactivate_feat: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:FEATure:DEACtivate?')
		return trim_str_response(response)

	def set_deactivate(self, deactivate_feat: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:FEATure:DEACtivate \n
		Snippet: driver.source.bb.nr5G.feature.set_deactivate(deactivate_feat = '1') \n
		No command help available \n
			:param deactivate_feat: No help available
		"""
		param = Conversions.value_to_quoted_str(deactivate_feat)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:FEATure:DEACtivate {param}')

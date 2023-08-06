from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dl:
	"""Dl commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dl", core, parent)

	def get_catalog(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SETTing:TMODel:DL:CATalog \n
		Snippet: value: List[str] = driver.source.bb.nr5G.setting.tmodel.dl.get_catalog() \n
		Queries the filenames of predefined files with test signals in the default directory. \n
			:return: nr_5_gcat_name_tmod_dn: filename1,filename2,... Returns a string of filenames separated by commas.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:SETTing:TMODel:DL:CATalog?')
		return Conversions.str_to_str_list(response)

	def get_value(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SETTing:TMODel:DL \n
		Snippet: value: str = driver.source.bb.nr5G.setting.tmodel.dl.get_value() \n
		Loads a test model file with predefined settings. \n
			:return: tmod_dn: 'filename' Filename as queried with one of the following commands: method RsSmbv.Source.Bb.Nr5G.Setting.Tmodel.Ul.catalog method RsSmbv.Source.Bb.Nr5G.Setting.Tmodel.Dl.catalog method RsSmbv.Source.Bb.Nr5G.Setting.Tmodel.FilterPy.catalog
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:SETTing:TMODel:DL?')
		return trim_str_response(response)

	def set_value(self, tmod_dn: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SETTing:TMODel:DL \n
		Snippet: driver.source.bb.nr5G.setting.tmodel.dl.set_value(tmod_dn = '1') \n
		Loads a test model file with predefined settings. \n
			:param tmod_dn: 'filename' Filename as queried with one of the following commands: method RsSmbv.Source.Bb.Nr5G.Setting.Tmodel.Ul.catalog method RsSmbv.Source.Bb.Nr5G.Setting.Tmodel.Dl.catalog method RsSmbv.Source.Bb.Nr5G.Setting.Tmodel.FilterPy.catalog
		"""
		param = Conversions.value_to_quoted_str(tmod_dn)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SETTing:TMODel:DL {param}')

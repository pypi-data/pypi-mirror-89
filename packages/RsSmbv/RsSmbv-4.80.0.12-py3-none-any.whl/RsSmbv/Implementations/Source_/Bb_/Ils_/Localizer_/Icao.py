from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Icao:
	"""Icao commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("icao", core, parent)

	# noinspection PyTypeChecker
	def get_channel(self) -> enums.AvionicIlsIcaoChan:
		"""SCPI: [SOURce<HW>]:[BB]:ILS:LOCalizer:ICAO:CHANnel \n
		Snippet: value: enums.AvionicIlsIcaoChan = driver.source.bb.ils.localizer.icao.get_channel() \n
		Sets the ICAO channel and the corresponding transmitting frequency. If avionic standard modulation is activated and you
		change the 'RF Frequency', the frequency value of the closest ICAO channel is applied automatically. The 'ICAO Channel'
		is also updated. The ICAO channel settings for ILS glide slope/localizer components are coupled. For an overview of the
		ILS ICAO channel frequencies, see Table 'ILS glide slope and localizer ICAO standard frequencies (MHz) and channels'. \n
			:return: sel_icao_chan: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ILS:LOCalizer:ICAO:CHANnel?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicIlsIcaoChan)

	def set_channel(self, sel_icao_chan: enums.AvionicIlsIcaoChan) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:ILS:LOCalizer:ICAO:CHANnel \n
		Snippet: driver.source.bb.ils.localizer.icao.set_channel(sel_icao_chan = enums.AvionicIlsIcaoChan.CH18X) \n
		Sets the ICAO channel and the corresponding transmitting frequency. If avionic standard modulation is activated and you
		change the 'RF Frequency', the frequency value of the closest ICAO channel is applied automatically. The 'ICAO Channel'
		is also updated. The ICAO channel settings for ILS glide slope/localizer components are coupled. For an overview of the
		ILS ICAO channel frequencies, see Table 'ILS glide slope and localizer ICAO standard frequencies (MHz) and channels'. \n
			:param sel_icao_chan: CH18X| CH18Y| CH20X| CH20Y| CH22X| CH22Y| CH24X| CH24Y| CH26X| CH26Y| CH28X| CH28Y| CH30X| CH30Y| CH32X| CH32Y| CH34X| CH34Y| CH36X| CH36Y| CH38X| CH38Y| CH40X| CH40Y| CH42X| CH42Y| CH44X| CH44Y| CH46X| CH46Y| CH48X| CH48Y| CH50X| CH50Y| CH52X| CH52Y| CH54X| CH54Y| CH56X| CH56Y
		"""
		param = Conversions.enum_scalar_to_str(sel_icao_chan, enums.AvionicIlsIcaoChan)
		self._core.io.write(f'SOURce<HwInstance>:BB:ILS:LOCalizer:ICAO:CHANnel {param}')

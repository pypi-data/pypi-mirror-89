from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Srs:
	"""Srs commands group definition. 6 total commands, 0 Sub-groups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("srs", core, parent)

	def get_anstx(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:REFSig:SRS:ANSTx \n
		Snippet: value: bool = driver.source.bb.eutra.ul.refsig.srs.get_anstx() \n
		Enables/disables simultaneous transmission of SRS (sounding reference signal) and ACK/NACK messages, i.e. transmission of
		SRS and PUCCH in the same subframe. \n
			:return: an_srs_sim_tx_state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:REFSig:SRS:ANSTx?')
		return Conversions.str_to_bool(response)

	def set_anstx(self, an_srs_sim_tx_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:REFSig:SRS:ANSTx \n
		Snippet: driver.source.bb.eutra.ul.refsig.srs.set_anstx(an_srs_sim_tx_state = False) \n
		Enables/disables simultaneous transmission of SRS (sounding reference signal) and ACK/NACK messages, i.e. transmission of
		SRS and PUCCH in the same subframe. \n
			:param an_srs_sim_tx_state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(an_srs_sim_tx_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:REFSig:SRS:ANSTx {param}')

	def get_csrs(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:REFSig:SRS:CSRS \n
		Snippet: value: int = driver.source.bb.eutra.ul.refsig.srs.get_csrs() \n
		Sets the cell-specific parameter SRS bandwidth configuration (CSRS) . \n
			:return: csrs: integer Range: 0 to 7
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:REFSig:SRS:CSRS?')
		return Conversions.str_to_int(response)

	def set_csrs(self, csrs: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:REFSig:SRS:CSRS \n
		Snippet: driver.source.bb.eutra.ul.refsig.srs.set_csrs(csrs = 1) \n
		Sets the cell-specific parameter SRS bandwidth configuration (CSRS) . \n
			:param csrs: integer Range: 0 to 7
		"""
		param = Conversions.decimal_value_to_str(csrs)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:REFSig:SRS:CSRS {param}')

	def get_dsfc(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:REFSig:SRS:DSFC \n
		Snippet: value: str = driver.source.bb.eutra.ul.refsig.srs.get_dsfc() \n
		Queries the value for the cell-specific parameter transmission offset DeltaSFC in subframes, depending on the selected
		SRS subframe configuration (method RsSmbv.Source.Bb.Eutra.Ul.Refsig.Srs.csrs) and the dduplexing mode (method RsSmbv.
		Source.Bb.Eutra.duplexing) . \n
			:return: delta_sfc: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:REFSig:SRS:DSFC?')
		return trim_str_response(response)

	def get_mu_pts(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:REFSig:SRS:MUPTs \n
		Snippet: value: bool = driver.source.bb.eutra.ul.refsig.srs.get_mu_pts() \n
		Enables/disables the cell-specific parameter srsMaxUpPts. \n
			:return: max_up_pts: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:REFSig:SRS:MUPTs?')
		return Conversions.str_to_bool(response)

	def set_mu_pts(self, max_up_pts: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:REFSig:SRS:MUPTs \n
		Snippet: driver.source.bb.eutra.ul.refsig.srs.set_mu_pts(max_up_pts = False) \n
		Enables/disables the cell-specific parameter srsMaxUpPts. \n
			:param max_up_pts: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(max_up_pts)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:REFSig:SRS:MUPTs {param}')

	def get_su_configuration(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:REFSig:SRS:SUConfiguration \n
		Snippet: value: int = driver.source.bb.eutra.ul.refsig.srs.get_su_configuration() \n
		Sets the cell-specific parameter SRS subframe configuration. \n
			:return: sub_frame_config: integer Range: 0 to 15
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:REFSig:SRS:SUConfiguration?')
		return Conversions.str_to_int(response)

	def set_su_configuration(self, sub_frame_config: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:REFSig:SRS:SUConfiguration \n
		Snippet: driver.source.bb.eutra.ul.refsig.srs.set_su_configuration(sub_frame_config = 1) \n
		Sets the cell-specific parameter SRS subframe configuration. \n
			:param sub_frame_config: integer Range: 0 to 15
		"""
		param = Conversions.decimal_value_to_str(sub_frame_config)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:REFSig:SRS:SUConfiguration {param}')

	def get_tsfc(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:REFSig:SRS:TSFC \n
		Snippet: value: str = driver.source.bb.eutra.ul.refsig.srs.get_tsfc() \n
		Queries the value for the cell-specific parameter configuration period TSFC in subframes, depending on the selected SRS
		subframe configuration (method RsSmbv.Source.Bb.Eutra.Ul.Refsig.Srs.csrs) and the duplexing mode (method RsSmbv.Source.Bb.
		Eutra.duplexing) . \n
			:return: tsfc: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:REFSig:SRS:TSFC?')
		return trim_str_response(response)

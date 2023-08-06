from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ant:
	"""Ant commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ant", core, parent)

	# noinspection PyTypeChecker
	def get_rx_antennas(self) -> enums.RxaNt:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:ANT:RXANtennas \n
		Snippet: value: enums.RxaNt = driver.source.bb.nr5G.tcw.ant.get_rx_antennas() \n
		Shows or sets the number of Rx antennas used for test case. \n
			:return: rx_antennas: ANT1| ANT2| ANT4| ANT8
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:ANT:RXANtennas?')
		return Conversions.str_to_scalar_enum(response, enums.RxaNt)

	def set_rx_antennas(self, rx_antennas: enums.RxaNt) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:ANT:RXANtennas \n
		Snippet: driver.source.bb.nr5G.tcw.ant.set_rx_antennas(rx_antennas = enums.RxaNt.ANT1) \n
		Shows or sets the number of Rx antennas used for test case. \n
			:param rx_antennas: ANT1| ANT2| ANT4| ANT8
		"""
		param = Conversions.enum_scalar_to_str(rx_antennas, enums.RxaNt)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:ANT:RXANtennas {param}')

	# noinspection PyTypeChecker
	def get_tx_antennas(self) -> enums.TxAntenna:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:ANT:TXANtennas \n
		Snippet: value: enums.TxAntenna = driver.source.bb.nr5G.tcw.ant.get_tx_antennas() \n
		Shows or sets the number of Tx antennas used for test case. \n
			:return: tx_antennas: ANT1| ANT2
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:ANT:TXANtennas?')
		return Conversions.str_to_scalar_enum(response, enums.TxAntenna)

	def set_tx_antennas(self, tx_antennas: enums.TxAntenna) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:ANT:TXANtennas \n
		Snippet: driver.source.bb.nr5G.tcw.ant.set_tx_antennas(tx_antennas = enums.TxAntenna.ANT1) \n
		Shows or sets the number of Tx antennas used for test case. \n
			:param tx_antennas: ANT1| ANT2
		"""
		param = Conversions.enum_scalar_to_str(tx_antennas, enums.TxAntenna)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:ANT:TXANtennas {param}')

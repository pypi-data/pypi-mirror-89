from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Isrs:
	"""Isrs commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("isrs", core, parent)

	def set(self, isrs: int, stream=repcap.Stream.Default, carrierComponent=repcap.CarrierComponent.Default, soundRefSignalIx=repcap.SoundRefSignalIx.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:[CELL<CCIDX>]:REFSig:SRS<SRSIDX_OPTIONAL>:ISRS \n
		Snippet: driver.source.bb.eutra.ul.ue.cell.refsig.srs.isrs.set(isrs = 1, stream = repcap.Stream.Default, carrierComponent = repcap.CarrierComponent.Default, soundRefSignalIx = repcap.SoundRefSignalIx.Default) \n
		Sets the UE-specific parameter SRS configuration index ISRS. \n
			:param isrs: integer Range: 0 to 1023
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param soundRefSignalIx: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Srs')"""
		param = Conversions.decimal_value_to_str(isrs)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		soundRefSignalIx_cmd_val = self._base.get_repcap_cmd_value(soundRefSignalIx, repcap.SoundRefSignalIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:CELL{carrierComponent_cmd_val}:REFSig:SRS{soundRefSignalIx_cmd_val}:ISRS {param}')

	def get(self, stream=repcap.Stream.Default, carrierComponent=repcap.CarrierComponent.Default, soundRefSignalIx=repcap.SoundRefSignalIx.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:[CELL<CCIDX>]:REFSig:SRS<SRSIDX_OPTIONAL>:ISRS \n
		Snippet: value: int = driver.source.bb.eutra.ul.ue.cell.refsig.srs.isrs.get(stream = repcap.Stream.Default, carrierComponent = repcap.CarrierComponent.Default, soundRefSignalIx = repcap.SoundRefSignalIx.Default) \n
		Sets the UE-specific parameter SRS configuration index ISRS. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param soundRefSignalIx: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Srs')
			:return: isrs: integer Range: 0 to 1023"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		soundRefSignalIx_cmd_val = self._base.get_repcap_cmd_value(soundRefSignalIx, repcap.SoundRefSignalIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:CELL{carrierComponent_cmd_val}:REFSig:SRS{soundRefSignalIx_cmd_val}:ISRS?')
		return Conversions.str_to_int(response)

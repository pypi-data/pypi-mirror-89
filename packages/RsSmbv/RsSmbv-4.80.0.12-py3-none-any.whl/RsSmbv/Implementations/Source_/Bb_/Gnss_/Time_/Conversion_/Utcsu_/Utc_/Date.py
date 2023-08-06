from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.StructBase import StructBase
from .........Internal.ArgStruct import ArgStruct
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Date:
	"""Date commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("date", core, parent)

	# noinspection PyTypeChecker
	class GetStruct(StructBase):
		"""Response structure. Fields: \n
			- Year: int: integer Range: 1996 to 9999
			- Month: int: integer Range: 1 to 12
			- Day: int: integer Range: 1 to 31"""
		__meta_args_list = [
			ArgStruct.scalar_int('Year'),
			ArgStruct.scalar_int('Month'),
			ArgStruct.scalar_int('Day')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Year: int = None
			self.Month: int = None
			self.Day: int = None

	def get(self, stream=repcap.Stream.Default) -> GetStruct:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TIME:CONVersion:UTCSu<ST>:UTC:DATE \n
		Snippet: value: GetStruct = driver.source.bb.gnss.time.conversion.utcsu.utc.date.get(stream = repcap.Stream.Default) \n
		Enters the date for the UTC-UTC(SU) data in DMS format. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Utcsu')
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:GNSS:TIME:CONVersion:UTCSu{stream_cmd_val}:UTC:DATE?', self.__class__.GetStruct())

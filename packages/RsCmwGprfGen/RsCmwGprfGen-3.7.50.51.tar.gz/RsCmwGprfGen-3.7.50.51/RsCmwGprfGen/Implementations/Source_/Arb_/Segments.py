from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Segments:
	"""Segments commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("segments", core, parent)

	def get_next(self) -> int:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:SEGMents:NEXT \n
		Snippet: value: int = driver.source.arb.segments.get_next() \n
		Selects a segment to be processed after the end of the currently processed segment. \n
			:return: segment_number: Range: 0 to not documented
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:ARB:SEGMents:NEXT?')
		return Conversions.str_to_int(response)

	def set_next(self, segment_number: int) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:SEGMents:NEXT \n
		Snippet: driver.source.arb.segments.set_next(segment_number = 1) \n
		Selects a segment to be processed after the end of the currently processed segment. \n
			:param segment_number: Range: 0 to not documented
		"""
		param = Conversions.decimal_value_to_str(segment_number)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:ARB:SEGMents:NEXT {param}')

	# noinspection PyTypeChecker
	class CurrentStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Segment_Number: int: Integer number. NAV is returned if no file is loaded. Range: 0 to 1000
			- Segment_Name: str: String parameter containing the name. NAV is returned if no file is loaded or no name is defined."""
		__meta_args_list = [
			ArgStruct.scalar_int('Segment_Number'),
			ArgStruct.scalar_str('Segment_Name')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Segment_Number: int = None
			self.Segment_Name: str = None

	def get_current(self) -> CurrentStruct:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:SEGMents:CURRent \n
		Snippet: value: CurrentStruct = driver.source.arb.segments.get_current() \n
		Queries the number and name of the currently processed segment. For the repetition 'Continuous Seamless', a trigger event
		has been received for the returned segment. The generator is still processing the previous segment or it is already
		processing the returned segment. For a distinction of the two cases, see method RsCmwGprfGen.Source.Arb.status. \n
			:return: structure: for return value, see the help for CurrentStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce:GPRF:GENerator<Instance>:ARB:SEGMents:CURRent?', self.__class__.CurrentStruct())

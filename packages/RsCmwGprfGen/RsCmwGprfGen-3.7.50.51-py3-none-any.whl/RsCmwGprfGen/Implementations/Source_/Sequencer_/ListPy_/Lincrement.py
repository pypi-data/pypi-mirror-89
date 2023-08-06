from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Types import DataType
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Lincrement:
	"""Lincrement commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lincrement", core, parent)

	def set(self, index: int, list_increment: enums.ListIncrement) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:LINCrement \n
		Snippet: driver.source.sequencer.listPy.lincrement.set(index = 1, list_increment = enums.ListIncrement.ACYCles) \n
		Defines or queries the list increment for the sequencer list entry with the selected <Index>. \n
			:param index: No help available
			:param list_increment: DTIMe | ACYCles | USER | MEASurement | TRIGger DTIMe Dwell time defined via method RsCmwGprfGen.Source.Sequencer.ListPy.Dtime.set ACYCles ARB cycles defined via method RsCmwGprfGen.Source.Sequencer.ListPy.Acycles.set USER User action triggered via method RsCmwGprfGen.Trigger.Sequencer.Manual.Execute.set MEASurement Measurement source selected via method RsCmwGprfGen.Trigger.Sequencer.IsMeas.source TRIGger Trigger source selected via method RsCmwGprfGen.Trigger.Sequencer.IsTrigger.source
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('index', index, DataType.Integer), ArgSingle('list_increment', list_increment, DataType.Enum))
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:LINCrement {param}'.rstrip())

	# noinspection PyTypeChecker
	def get(self, index: int) -> enums.ListIncrement:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:LINCrement \n
		Snippet: value: enums.ListIncrement = driver.source.sequencer.listPy.lincrement.get(index = 1) \n
		Defines or queries the list increment for the sequencer list entry with the selected <Index>. \n
			:param index: No help available
			:return: list_increment: DTIMe | ACYCles | USER | MEASurement | TRIGger DTIMe Dwell time defined via method RsCmwGprfGen.Source.Sequencer.ListPy.Dtime.set ACYCles ARB cycles defined via method RsCmwGprfGen.Source.Sequencer.ListPy.Acycles.set USER User action triggered via method RsCmwGprfGen.Trigger.Sequencer.Manual.Execute.set MEASurement Measurement source selected via method RsCmwGprfGen.Trigger.Sequencer.IsMeas.source TRIGger Trigger source selected via method RsCmwGprfGen.Trigger.Sequencer.IsTrigger.source"""
		param = Conversions.decimal_value_to_str(index)
		response = self._core.io.query_str(f'SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:LINCrement? {param}')
		return Conversions.str_to_scalar_enum(response, enums.ListIncrement)

	# noinspection PyTypeChecker
	def get_all(self) -> List[enums.ListIncrement]:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:LINCrement:ALL \n
		Snippet: value: List[enums.ListIncrement] = driver.source.sequencer.listPy.lincrement.get_all() \n
		Defines the list increments for all sequencer list entries. \n
			:return: list_increment: DTIMe | ACYCles | USER | MEASurement | TRIGger Comma-separated list of values, one value per list entry DTIMe Dwell time defined via method RsCmwGprfGen.Source.Sequencer.ListPy.Dtime.all ACYCles ARB cycles defined via method RsCmwGprfGen.Source.Sequencer.ListPy.Acycles.all USER User action triggered via method RsCmwGprfGen.Trigger.Sequencer.Manual.Execute.set MEASurement Measurement source selected via method RsCmwGprfGen.Trigger.Sequencer.IsMeas.source TRIGger Trigger source selected via method RsCmwGprfGen.Trigger.Sequencer.IsTrigger.source
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:LINCrement:ALL?')
		return Conversions.str_to_list_enum(response, enums.ListIncrement)

	def set_all(self, list_increment: List[enums.ListIncrement]) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:LINCrement:ALL \n
		Snippet: driver.source.sequencer.listPy.lincrement.set_all(list_increment = [ListIncrement.ACYCles, ListIncrement.USER]) \n
		Defines the list increments for all sequencer list entries. \n
			:param list_increment: DTIMe | ACYCles | USER | MEASurement | TRIGger Comma-separated list of values, one value per list entry DTIMe Dwell time defined via method RsCmwGprfGen.Source.Sequencer.ListPy.Dtime.all ACYCles ARB cycles defined via method RsCmwGprfGen.Source.Sequencer.ListPy.Acycles.all USER User action triggered via method RsCmwGprfGen.Trigger.Sequencer.Manual.Execute.set MEASurement Measurement source selected via method RsCmwGprfGen.Trigger.Sequencer.IsMeas.source TRIGger Trigger source selected via method RsCmwGprfGen.Trigger.Sequencer.IsTrigger.source
		"""
		param = Conversions.enum_list_to_str(list_increment, enums.ListIncrement)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:LINCrement:ALL {param}')

from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Types import DataType
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dtime:
	"""Dtime commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dtime", core, parent)

	def set(self, index: int, dwelltime: float) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:DTIMe \n
		Snippet: driver.source.listPy.dtime.set(index = 1, dwelltime = 1.0) \n
		Defines or queries the transmission time for a selected frequency/level step in 'Dwell Time' mode. The value is not used
		in the other list modes (see method RsCmwGprfGen.Source.ListPy.Increment.value) . \n
			:param index: Number of the frequency/level step in the table Range: 0 to 1999
			:param dwelltime: Dwell time for the frequency/level step Range: 200E-6 s to 20 s, Unit: s
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('index', index, DataType.Integer), ArgSingle('dwelltime', dwelltime, DataType.Float))
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:LIST:DTIMe {param}'.rstrip())

	def get(self, index: int) -> float:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:DTIMe \n
		Snippet: value: float = driver.source.listPy.dtime.get(index = 1) \n
		Defines or queries the transmission time for a selected frequency/level step in 'Dwell Time' mode. The value is not used
		in the other list modes (see method RsCmwGprfGen.Source.ListPy.Increment.value) . \n
			:param index: Number of the frequency/level step in the table Range: 0 to 1999
			:return: dwelltime: Dwell time for the frequency/level step Range: 200E-6 s to 20 s, Unit: s"""
		param = Conversions.decimal_value_to_str(index)
		response = self._core.io.query_str(f'SOURce:GPRF:GENerator<Instance>:LIST:DTIMe? {param}')
		return Conversions.str_to_float(response)

	def get_all(self) -> List[float]:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:DTIMe:ALL \n
		Snippet: value: List[float] = driver.source.listPy.dtime.get_all() \n
		Defines the transmission times for all frequency/level steps in 'Dwell Time' mode. The value is not used in the other
		list modes (see method RsCmwGprfGen.Source.ListPy.Increment.value) . \n
			:return: all_dwelltimes: Comma-separated list of n values, one per frequency/level step, where n 2001. The query returns 2000 results. Range: 200E-6 s to 20 s, Unit: s
		"""
		response = self._core.io.query_bin_or_ascii_float_list('SOURce:GPRF:GENerator<Instance>:LIST:DTIMe:ALL?')
		return response

	def set_all(self, all_dwelltimes: List[float]) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:DTIMe:ALL \n
		Snippet: driver.source.listPy.dtime.set_all(all_dwelltimes = [1.1, 2.2, 3.3]) \n
		Defines the transmission times for all frequency/level steps in 'Dwell Time' mode. The value is not used in the other
		list modes (see method RsCmwGprfGen.Source.ListPy.Increment.value) . \n
			:param all_dwelltimes: Comma-separated list of n values, one per frequency/level step, where n 2001. The query returns 2000 results. Range: 200E-6 s to 20 s, Unit: s
		"""
		param = Conversions.list_to_csv_str(all_dwelltimes)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:LIST:DTIMe:ALL {param}')

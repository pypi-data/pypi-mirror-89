from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Types import DataType
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Acycles:
	"""Acycles commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("acycles", core, parent)

	def set(self, index: int, arb_cycles: int) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:ACYCles \n
		Snippet: driver.source.sequencer.listPy.acycles.set(index = 1, arb_cycles = 1) \n
		Defines or queries the number of ARB cycles for the sequencer list entry with the selected <Index>. \n
			:param index: No help available
			:param arb_cycles: Range: 1 to 10000
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('index', index, DataType.Integer), ArgSingle('arb_cycles', arb_cycles, DataType.Integer))
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:ACYCles {param}'.rstrip())

	def get(self, index: int) -> int:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:ACYCles \n
		Snippet: value: int = driver.source.sequencer.listPy.acycles.get(index = 1) \n
		Defines or queries the number of ARB cycles for the sequencer list entry with the selected <Index>. \n
			:param index: No help available
			:return: arb_cycles: Range: 1 to 10000"""
		param = Conversions.decimal_value_to_str(index)
		response = self._core.io.query_str(f'SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:ACYCles? {param}')
		return Conversions.str_to_int(response)

	def get_all(self) -> List[int]:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:ACYCles:ALL \n
		Snippet: value: List[int] = driver.source.sequencer.listPy.acycles.get_all() \n
		Defines the ARB cycles for all sequencer list entries. \n
			:return: arb_cycles: Comma-separated list of values, one value per list entry Range: 1 to 10000
		"""
		response = self._core.io.query_bin_or_ascii_int_list('SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:ACYCles:ALL?')
		return response

	def set_all(self, arb_cycles: List[int]) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:ACYCles:ALL \n
		Snippet: driver.source.sequencer.listPy.acycles.set_all(arb_cycles = [1, 2, 3]) \n
		Defines the ARB cycles for all sequencer list entries. \n
			:param arb_cycles: Comma-separated list of values, one value per list entry Range: 1 to 10000
		"""
		param = Conversions.list_to_csv_str(arb_cycles)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:ACYCles:ALL {param}')

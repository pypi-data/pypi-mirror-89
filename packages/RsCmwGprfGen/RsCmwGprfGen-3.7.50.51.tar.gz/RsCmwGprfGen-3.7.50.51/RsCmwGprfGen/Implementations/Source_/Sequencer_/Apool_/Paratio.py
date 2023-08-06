from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Paratio:
	"""Paratio commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("paratio", core, parent)

	def get_all(self) -> List[float]:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:APOol:PARatio:ALL \n
		Snippet: value: List[float] = driver.source.sequencer.apool.paratio.get_all() \n
		Queries the peak to average ratios of the ARB files in the file pool. \n
			:return: peak_avg_ratio: Comma-separated list of values, one value per file Unit: dB
		"""
		response = self._core.io.query_bin_or_ascii_float_list('SOURce:GPRF:GENerator<Instance>:SEQuencer:APOol:PARatio:ALL?')
		return response

	def get(self, index: int) -> float:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:APOol:PARatio \n
		Snippet: value: float = driver.source.sequencer.apool.paratio.get(index = 1) \n
		Queries the peak to average ratio of the ARB file with the specified <Index>. \n
			:param index: Unit: dB
			:return: peak_avg_ratio: Unit: dB"""
		param = Conversions.decimal_value_to_str(index)
		response = self._core.io.query_str(f'SOURce:GPRF:GENerator<Instance>:SEQuencer:APOol:PARatio? {param}')
		return Conversions.str_to_float(response)

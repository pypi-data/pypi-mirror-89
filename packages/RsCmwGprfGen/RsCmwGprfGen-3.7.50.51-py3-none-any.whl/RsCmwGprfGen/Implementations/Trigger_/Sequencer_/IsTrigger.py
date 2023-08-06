from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IsTrigger:
	"""IsTrigger commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("isTrigger", core, parent)

	def get_catalog(self) -> List[str]:
		"""SCPI: TRIGger:GPRF:GENerator<Instance>:SEQuencer:ISTRigger:CATalog \n
		Snippet: value: List[str] = driver.trigger.sequencer.isTrigger.get_catalog() \n
		Queries all available trigger source strings. \n
			:return: source_list: Comma-separated list of strings. Each string represents a supported source.
		"""
		response = self._core.io.query_str('TRIGger:GPRF:GENerator<Instance>:SEQuencer:ISTRigger:CATalog?')
		return Conversions.str_to_str_list(response)

	def get_source(self) -> str:
		"""SCPI: TRIGger:GPRF:GENerator<Instance>:SEQuencer:ISTRigger:SOURce \n
		Snippet: value: str = driver.trigger.sequencer.isTrigger.get_source() \n
		Selects a trigger source for triggering sequencer list incrementations. A complete list of all supported strings can be
		queried using method RsCmwGprfGen.Trigger.Sequencer.IsTrigger.catalog. \n
			:return: source: Trigger source as string
		"""
		response = self._core.io.query_str('TRIGger:GPRF:GENerator<Instance>:SEQuencer:ISTRigger:SOURce?')
		return trim_str_response(response)

	def set_source(self, source: str) -> None:
		"""SCPI: TRIGger:GPRF:GENerator<Instance>:SEQuencer:ISTRigger:SOURce \n
		Snippet: driver.trigger.sequencer.isTrigger.set_source(source = '1') \n
		Selects a trigger source for triggering sequencer list incrementations. A complete list of all supported strings can be
		queried using method RsCmwGprfGen.Trigger.Sequencer.IsTrigger.catalog. \n
			:param source: Trigger source as string
		"""
		param = Conversions.value_to_quoted_str(source)
		self._core.io.write(f'TRIGger:GPRF:GENerator<Instance>:SEQuencer:ISTRigger:SOURce {param}')

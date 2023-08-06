from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dgain:
	"""Dgain commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dgain", core, parent)

	def get_svalue(self) -> float:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:FILL:DGAin:SVALue \n
		Snippet: value: float = driver.source.sequencer.listPy.fill.dgain.get_svalue() \n
		Configures the start value for filling the sequencer list with digital gain values. \n
			:return: start_value: Range: -30 dB to 0 dB, Unit: dB
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:FILL:DGAin:SVALue?')
		return Conversions.str_to_float(response)

	def set_svalue(self, start_value: float) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:FILL:DGAin:SVALue \n
		Snippet: driver.source.sequencer.listPy.fill.dgain.set_svalue(start_value = 1.0) \n
		Configures the start value for filling the sequencer list with digital gain values. \n
			:param start_value: Range: -30 dB to 0 dB, Unit: dB
		"""
		param = Conversions.decimal_value_to_str(start_value)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:FILL:DGAin:SVALue {param}')

	def get_increment(self) -> float:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:FILL:DGAin:INCRement \n
		Snippet: value: float = driver.source.sequencer.listPy.fill.dgain.get_increment() \n
		Configures the increment for filling the sequencer list with digital gain values. \n
			:return: increment: Range: Depends on the number of entries and on the start value , Unit: dB
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:FILL:DGAin:INCRement?')
		return Conversions.str_to_float(response)

	def set_increment(self, increment: float) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:FILL:DGAin:INCRement \n
		Snippet: driver.source.sequencer.listPy.fill.dgain.set_increment(increment = 1.0) \n
		Configures the increment for filling the sequencer list with digital gain values. \n
			:param increment: Range: Depends on the number of entries and on the start value , Unit: dB
		"""
		param = Conversions.decimal_value_to_str(increment)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:FILL:DGAin:INCRement {param}')

	def get_keep(self) -> bool:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:FILL:DGAin:KEEP \n
		Snippet: value: bool = driver.source.sequencer.listPy.fill.dgain.get_keep() \n
		Selects whether the digital gain of existing entries is kept or overwritten when the sequencer list is filled. \n
			:return: keep_flag: OFF | ON OFF: overwrite values ON: keep values
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:FILL:DGAin:KEEP?')
		return Conversions.str_to_bool(response)

	def set_keep(self, keep_flag: bool) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:FILL:DGAin:KEEP \n
		Snippet: driver.source.sequencer.listPy.fill.dgain.set_keep(keep_flag = False) \n
		Selects whether the digital gain of existing entries is kept or overwritten when the sequencer list is filled. \n
			:param keep_flag: OFF | ON OFF: overwrite values ON: keep values
		"""
		param = Conversions.bool_to_str(keep_flag)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:FILL:DGAin:KEEP {param}')

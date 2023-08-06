from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Segments:
	"""Segments commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("segments", core, parent)

	@property
	def manual(self):
		"""manual commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_manual'):
			from .Segments_.Manual import Manual
			self._manual = Manual(self._core, self._base)
		return self._manual

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.ArbSegmentsMode:
		"""SCPI: TRIGger:GPRF:GENerator<Instance>:ARB:SEGMents:MODE \n
		Snippet: value: enums.ArbSegmentsMode = driver.trigger.arb.segments.get_mode() \n
		Selects a trigger mode for multi-segment waveform files. \n
			:return: mode: CONTinuous | CSEamless | AUTO CONTinuous: A trigger event causes immediate switchover to the next segment CSEamless: A trigger event causes switchover after the end of the segment has been reached AUTO: The generator processes one segment after another
		"""
		response = self._core.io.query_str('TRIGger:GPRF:GENerator<Instance>:ARB:SEGMents:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.ArbSegmentsMode)

	def set_mode(self, mode: enums.ArbSegmentsMode) -> None:
		"""SCPI: TRIGger:GPRF:GENerator<Instance>:ARB:SEGMents:MODE \n
		Snippet: driver.trigger.arb.segments.set_mode(mode = enums.ArbSegmentsMode.AUTO) \n
		Selects a trigger mode for multi-segment waveform files. \n
			:param mode: CONTinuous | CSEamless | AUTO CONTinuous: A trigger event causes immediate switchover to the next segment CSEamless: A trigger event causes switchover after the end of the segment has been reached AUTO: The generator processes one segment after another
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.ArbSegmentsMode)
		self._core.io.write(f'TRIGger:GPRF:GENerator<Instance>:ARB:SEGMents:MODE {param}')

	def clone(self) -> 'Segments':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Segments(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Arb:
	"""Arb commands group definition. 9 total commands, 3 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("arb", core, parent)

	@property
	def catalog(self):
		"""catalog commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_catalog'):
			from .Arb_.Catalog import Catalog
			self._catalog = Catalog(self._core, self._base)
		return self._catalog

	@property
	def manual(self):
		"""manual commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_manual'):
			from .Arb_.Manual import Manual
			self._manual = Manual(self._core, self._base)
		return self._manual

	@property
	def segments(self):
		"""segments commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_segments'):
			from .Arb_.Segments import Segments
			self._segments = Segments(self._core, self._base)
		return self._segments

	# noinspection PyTypeChecker
	def get_slope(self) -> enums.SignalSlope:
		"""SCPI: TRIGger:GPRF:GENerator<Instance>:ARB:SLOPe \n
		Snippet: value: enums.SignalSlope = driver.trigger.arb.get_slope() \n
		Qualifies whether the trigger event is generated at the rising or at the falling edge of the trigger pulse. \n
			:return: slope: REDGe | FEDGe REDGe: Rising edge FEDGe: Falling edge
		"""
		response = self._core.io.query_str('TRIGger:GPRF:GENerator<Instance>:ARB:SLOPe?')
		return Conversions.str_to_scalar_enum(response, enums.SignalSlope)

	def set_slope(self, slope: enums.SignalSlope) -> None:
		"""SCPI: TRIGger:GPRF:GENerator<Instance>:ARB:SLOPe \n
		Snippet: driver.trigger.arb.set_slope(slope = enums.SignalSlope.FEDGe) \n
		Qualifies whether the trigger event is generated at the rising or at the falling edge of the trigger pulse. \n
			:param slope: REDGe | FEDGe REDGe: Rising edge FEDGe: Falling edge
		"""
		param = Conversions.enum_scalar_to_str(slope, enums.SignalSlope)
		self._core.io.write(f'TRIGger:GPRF:GENerator<Instance>:ARB:SLOPe {param}')

	def get_delay(self) -> float:
		"""SCPI: TRIGger:GPRF:GENerator<Instance>:ARB:DELay \n
		Snippet: value: float = driver.trigger.arb.get_delay() \n
		Sets/gets the trigger delay for the arbitrary RF generator, i.e. the time delaying the start of the generator relative to
		the selected trigger event. The delay does not apply to manual execution (see method RsCmwGprfGen.Trigger.Arb.Segments.
		Manual.Execute.set) . \n
			:return: delay: Range: 0 s to 100 s, Unit: s
		"""
		response = self._core.io.query_str('TRIGger:GPRF:GENerator<Instance>:ARB:DELay?')
		return Conversions.str_to_float(response)

	def set_delay(self, delay: float) -> None:
		"""SCPI: TRIGger:GPRF:GENerator<Instance>:ARB:DELay \n
		Snippet: driver.trigger.arb.set_delay(delay = 1.0) \n
		Sets/gets the trigger delay for the arbitrary RF generator, i.e. the time delaying the start of the generator relative to
		the selected trigger event. The delay does not apply to manual execution (see method RsCmwGprfGen.Trigger.Arb.Segments.
		Manual.Execute.set) . \n
			:param delay: Range: 0 s to 100 s, Unit: s
		"""
		param = Conversions.decimal_value_to_str(delay)
		self._core.io.write(f'TRIGger:GPRF:GENerator<Instance>:ARB:DELay {param}')

	def get_source(self) -> str:
		"""SCPI: TRIGger:GPRF:GENerator<Instance>:ARB:SOURce \n
		Snippet: value: str = driver.trigger.arb.get_source() \n
		Selects the source of the trigger events. Some values are always available in this firmware application. They are listed
		below. Depending on the installed options, additional values can be available. A complete list of all supported values
		can be displayed using method RsCmwGprfGen.Trigger.Arb.Catalog.source. \n
			:return: source: 'Manual' Manual trigger via GPRF generator GUI 'Base1: Cont.10ms Trigger' Periodical trigger signal with a trigger pulse every 10 ms 'Base1: User Trigger 1', 'Base1: User Trigger 2' TRIGger:BASE:UINitiatedn:EXECute
		"""
		response = self._core.io.query_str('TRIGger:GPRF:GENerator<Instance>:ARB:SOURce?')
		return trim_str_response(response)

	def set_source(self, source: str) -> None:
		"""SCPI: TRIGger:GPRF:GENerator<Instance>:ARB:SOURce \n
		Snippet: driver.trigger.arb.set_source(source = '1') \n
		Selects the source of the trigger events. Some values are always available in this firmware application. They are listed
		below. Depending on the installed options, additional values can be available. A complete list of all supported values
		can be displayed using method RsCmwGprfGen.Trigger.Arb.Catalog.source. \n
			:param source: 'Manual' Manual trigger via GPRF generator GUI 'Base1: Cont.10ms Trigger' Periodical trigger signal with a trigger pulse every 10 ms 'Base1: User Trigger 1', 'Base1: User Trigger 2' TRIGger:BASE:UINitiatedn:EXECute
		"""
		param = Conversions.value_to_quoted_str(source)
		self._core.io.write(f'TRIGger:GPRF:GENerator<Instance>:ARB:SOURce {param}')

	def get_re_trigger(self) -> bool:
		"""SCPI: TRIGger:GPRF:GENerator<Instance>:ARB:RETRigger \n
		Snippet: value: bool = driver.trigger.arb.get_re_trigger() \n
		Enables or disables the trigger system for waveform files. \n
			:return: retrigger: OFF | ON Trigger system disabled or enabled
		"""
		response = self._core.io.query_str('TRIGger:GPRF:GENerator<Instance>:ARB:RETRigger?')
		return Conversions.str_to_bool(response)

	def set_re_trigger(self, retrigger: bool) -> None:
		"""SCPI: TRIGger:GPRF:GENerator<Instance>:ARB:RETRigger \n
		Snippet: driver.trigger.arb.set_re_trigger(retrigger = False) \n
		Enables or disables the trigger system for waveform files. \n
			:param retrigger: OFF | ON Trigger system disabled or enabled
		"""
		param = Conversions.bool_to_str(retrigger)
		self._core.io.write(f'TRIGger:GPRF:GENerator<Instance>:ARB:RETRigger {param}')

	def get_autostart(self) -> bool:
		"""SCPI: TRIGger:GPRF:GENerator<Instance>:ARB:AUTostart \n
		Snippet: value: bool = driver.trigger.arb.get_autostart() \n
		Enables or disables the automatic download of the selected (and loaded) waveform file whenever the generator is turned on. \n
			:return: autostart: OFF | ON Autostart disabled or enabled
		"""
		response = self._core.io.query_str('TRIGger:GPRF:GENerator<Instance>:ARB:AUTostart?')
		return Conversions.str_to_bool(response)

	def set_autostart(self, autostart: bool) -> None:
		"""SCPI: TRIGger:GPRF:GENerator<Instance>:ARB:AUTostart \n
		Snippet: driver.trigger.arb.set_autostart(autostart = False) \n
		Enables or disables the automatic download of the selected (and loaded) waveform file whenever the generator is turned on. \n
			:param autostart: OFF | ON Autostart disabled or enabled
		"""
		param = Conversions.bool_to_str(autostart)
		self._core.io.write(f'TRIGger:GPRF:GENerator<Instance>:ARB:AUTostart {param}')

	def clone(self) -> 'Arb':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Arb(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

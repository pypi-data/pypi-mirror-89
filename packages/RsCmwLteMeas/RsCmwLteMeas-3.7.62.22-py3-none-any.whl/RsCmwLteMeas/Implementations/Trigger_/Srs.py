from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Srs:
	"""Srs commands group definition. 6 total commands, 1 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("srs", core, parent)

	@property
	def catalog(self):
		"""catalog commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_catalog'):
			from .Srs_.Catalog import Catalog
			self._catalog = Catalog(self._core, self._base)
		return self._catalog

	def get_source(self) -> str:
		"""SCPI: TRIGger:LTE:MEASurement<Instance>:SRS:SOURce \n
		Snippet: value: str = driver.trigger.srs.get_source() \n
		Selects the source of the trigger events. Some values are always available in this firmware application. They are listed
		below. Depending on the installed options, additional values are available. A complete list of all supported values can
		be displayed using TRIGger:...:CATalog:SOURce?. \n
			:return: source: 'IF Power': Power trigger (received RF power)
		"""
		response = self._core.io.query_str('TRIGger:LTE:MEASurement<Instance>:SRS:SOURce?')
		return trim_str_response(response)

	def set_source(self, source: str) -> None:
		"""SCPI: TRIGger:LTE:MEASurement<Instance>:SRS:SOURce \n
		Snippet: driver.trigger.srs.set_source(source = '1') \n
		Selects the source of the trigger events. Some values are always available in this firmware application. They are listed
		below. Depending on the installed options, additional values are available. A complete list of all supported values can
		be displayed using TRIGger:...:CATalog:SOURce?. \n
			:param source: 'IF Power': Power trigger (received RF power)
		"""
		param = Conversions.value_to_quoted_str(source)
		self._core.io.write(f'TRIGger:LTE:MEASurement<Instance>:SRS:SOURce {param}')

	def get_threshold(self) -> float or bool:
		"""SCPI: TRIGger:LTE:MEASurement<Instance>:SRS:THReshold \n
		Snippet: value: float or bool = driver.trigger.srs.get_threshold() \n
		Defines the trigger threshold for power trigger sources. \n
			:return: trig_threshold: Range: -50 dB to 0 dB, Unit: dB (full scale, i.e. relative to reference level minus external attenuation)
		"""
		response = self._core.io.query_str('TRIGger:LTE:MEASurement<Instance>:SRS:THReshold?')
		return Conversions.str_to_float_or_bool(response)

	def set_threshold(self, trig_threshold: float or bool) -> None:
		"""SCPI: TRIGger:LTE:MEASurement<Instance>:SRS:THReshold \n
		Snippet: driver.trigger.srs.set_threshold(trig_threshold = 1.0) \n
		Defines the trigger threshold for power trigger sources. \n
			:param trig_threshold: Range: -50 dB to 0 dB, Unit: dB (full scale, i.e. relative to reference level minus external attenuation)
		"""
		param = Conversions.decimal_or_bool_value_to_str(trig_threshold)
		self._core.io.write(f'TRIGger:LTE:MEASurement<Instance>:SRS:THReshold {param}')

	# noinspection PyTypeChecker
	def get_slope(self) -> enums.SignalSlope:
		"""SCPI: TRIGger:LTE:MEASurement<Instance>:SRS:SLOPe \n
		Snippet: value: enums.SignalSlope = driver.trigger.srs.get_slope() \n
		Qualifies whether the trigger event is generated at the rising or at the falling edge of the trigger pulse (valid for
		external and power trigger sources) . \n
			:return: slope: REDGe | FEDGe REDGe: Rising edge FEDGe: Falling edge
		"""
		response = self._core.io.query_str('TRIGger:LTE:MEASurement<Instance>:SRS:SLOPe?')
		return Conversions.str_to_scalar_enum(response, enums.SignalSlope)

	def set_slope(self, slope: enums.SignalSlope) -> None:
		"""SCPI: TRIGger:LTE:MEASurement<Instance>:SRS:SLOPe \n
		Snippet: driver.trigger.srs.set_slope(slope = enums.SignalSlope.FEDGe) \n
		Qualifies whether the trigger event is generated at the rising or at the falling edge of the trigger pulse (valid for
		external and power trigger sources) . \n
			:param slope: REDGe | FEDGe REDGe: Rising edge FEDGe: Falling edge
		"""
		param = Conversions.enum_scalar_to_str(slope, enums.SignalSlope)
		self._core.io.write(f'TRIGger:LTE:MEASurement<Instance>:SRS:SLOPe {param}')

	def get_timeout(self) -> float or bool:
		"""SCPI: TRIGger:LTE:MEASurement<Instance>:SRS:TOUT \n
		Snippet: value: float or bool = driver.trigger.srs.get_timeout() \n
		Selects the maximum time that the R&S CMW waits for a trigger event before it stops the measurement in remote control
		mode or indicates a trigger timeout in manual operation mode. This setting has no influence on 'Free Run' measurements. \n
			:return: trigger_time_out: Range: 0.01 s to 167772.15 s, Unit: s Additional parameters: OFF | ON (disables | enables the timeout)
		"""
		response = self._core.io.query_str('TRIGger:LTE:MEASurement<Instance>:SRS:TOUT?')
		return Conversions.str_to_float_or_bool(response)

	def set_timeout(self, trigger_time_out: float or bool) -> None:
		"""SCPI: TRIGger:LTE:MEASurement<Instance>:SRS:TOUT \n
		Snippet: driver.trigger.srs.set_timeout(trigger_time_out = 1.0) \n
		Selects the maximum time that the R&S CMW waits for a trigger event before it stops the measurement in remote control
		mode or indicates a trigger timeout in manual operation mode. This setting has no influence on 'Free Run' measurements. \n
			:param trigger_time_out: Range: 0.01 s to 167772.15 s, Unit: s Additional parameters: OFF | ON (disables | enables the timeout)
		"""
		param = Conversions.decimal_or_bool_value_to_str(trigger_time_out)
		self._core.io.write(f'TRIGger:LTE:MEASurement<Instance>:SRS:TOUT {param}')

	def get_mgap(self) -> float:
		"""SCPI: TRIGger:LTE:MEASurement<Instance>:SRS:MGAP \n
		Snippet: value: float = driver.trigger.srs.get_mgap() \n
		Sets a minimum time during which the IF signal must be below the trigger threshold before the trigger is armed so that an
		IF power trigger event can be generated. \n
			:return: min_trig_gap: Range: 0 s to 1E-3 s, Unit: s
		"""
		response = self._core.io.query_str('TRIGger:LTE:MEASurement<Instance>:SRS:MGAP?')
		return Conversions.str_to_float(response)

	def set_mgap(self, min_trig_gap: float) -> None:
		"""SCPI: TRIGger:LTE:MEASurement<Instance>:SRS:MGAP \n
		Snippet: driver.trigger.srs.set_mgap(min_trig_gap = 1.0) \n
		Sets a minimum time during which the IF signal must be below the trigger threshold before the trigger is armed so that an
		IF power trigger event can be generated. \n
			:param min_trig_gap: Range: 0 s to 1E-3 s, Unit: s
		"""
		param = Conversions.decimal_value_to_str(min_trig_gap)
		self._core.io.write(f'TRIGger:LTE:MEASurement<Instance>:SRS:MGAP {param}')

	def clone(self) -> 'Srs':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Srs(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

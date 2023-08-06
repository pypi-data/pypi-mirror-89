from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Modulation:
	"""Modulation commands group definition. 9 total commands, 3 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("modulation", core, parent)

	@property
	def ewLength(self):
		"""ewLength commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_ewLength'):
			from .Modulation_.EwLength import EwLength
			self._ewLength = EwLength(self._core, self._base)
		return self._ewLength

	@property
	def eePeriods(self):
		"""eePeriods commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_eePeriods'):
			from .Modulation_.EePeriods import EePeriods
			self._eePeriods = EePeriods(self._core, self._base)
		return self._eePeriods

	@property
	def carrierAggregation(self):
		"""carrierAggregation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_carrierAggregation'):
			from .Modulation_.CarrierAggregation import CarrierAggregation
			self._carrierAggregation = CarrierAggregation(self._core, self._base)
		return self._carrierAggregation

	def get_equalizer(self) -> bool:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:MODulation:EQUalizer \n
		Snippet: value: bool = driver.configure.multiEval.modulation.get_equalizer() \n
		Enables or disables the post-FFT equalization step for the measurement of modulation results. \n
			:return: enable: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:MEValuation:MODulation:EQUalizer?')
		return Conversions.str_to_bool(response)

	def set_equalizer(self, enable: bool) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:MODulation:EQUalizer \n
		Snippet: driver.configure.multiEval.modulation.set_equalizer(enable = False) \n
		Enables or disables the post-FFT equalization step for the measurement of modulation results. \n
			:param enable: OFF | ON
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:MODulation:EQUalizer {param}')

	# noinspection PyTypeChecker
	def get_mscheme(self) -> enums.ModScheme:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:MODulation:MSCHeme \n
		Snippet: value: enums.ModScheme = driver.configure.multiEval.modulation.get_mscheme() \n
		Selects the modulation scheme used by the measured signal. \n
			:return: mod_scheme: AUTO | QPSK | Q16 | Q64 | Q256 Auto-detection, QPSK, 16-QAM, 64-QAM, 256-QAM
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:MEValuation:MODulation:MSCHeme?')
		return Conversions.str_to_scalar_enum(response, enums.ModScheme)

	def set_mscheme(self, mod_scheme: enums.ModScheme) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:MODulation:MSCHeme \n
		Snippet: driver.configure.multiEval.modulation.set_mscheme(mod_scheme = enums.ModScheme.AUTO) \n
		Selects the modulation scheme used by the measured signal. \n
			:param mod_scheme: AUTO | QPSK | Q16 | Q64 | Q256 Auto-detection, QPSK, 16-QAM, 64-QAM, 256-QAM
		"""
		param = Conversions.enum_scalar_to_str(mod_scheme, enums.ModScheme)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:MODulation:MSCHeme {param}')

	# noinspection PyTypeChecker
	def get_llocation(self) -> enums.LocalOscLocation:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:MODulation:LLOCation \n
		Snippet: value: enums.LocalOscLocation = driver.configure.multiEval.modulation.get_llocation() \n
		Specifies the UE transmitter architecture (local oscillator location) used for eMTC. \n
			:return: value: CN | CCB CN: Center of narrowband CCB: Center of cell bandwidth
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:MEValuation:MODulation:LLOCation?')
		return Conversions.str_to_scalar_enum(response, enums.LocalOscLocation)

	def set_llocation(self, value: enums.LocalOscLocation) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:MODulation:LLOCation \n
		Snippet: driver.configure.multiEval.modulation.set_llocation(value = enums.LocalOscLocation.CCB) \n
		Specifies the UE transmitter architecture (local oscillator location) used for eMTC. \n
			:param value: CN | CCB CN: Center of narrowband CCB: Center of cell bandwidth
		"""
		param = Conversions.enum_scalar_to_str(value, enums.LocalOscLocation)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:MODulation:LLOCation {param}')

	def clone(self) -> 'Modulation':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Modulation(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pusch:
	"""Pusch commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pusch", core, parent)

	# noinspection PyTypeChecker
	def get_leading(self) -> enums.LeadingExclPeriod:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:MODulation:EEPeriods:PUSCh:LEADing \n
		Snippet: value: enums.LeadingExclPeriod = driver.configure.multiEval.modulation.eePeriods.pusch.get_leading() \n
		Specifies an EVM exclusion period at the beginning of a subframe (detected channel type 'PUSCH') . The specified period
		is excluded from the calculation of EVM, magnitude error and phase error results. \n
			:return: leading: OFF | MS25 OFF: no exclusion MS25: 25 μs excluded
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:MEValuation:MODulation:EEPeriods:PUSCh:LEADing?')
		return Conversions.str_to_scalar_enum(response, enums.LeadingExclPeriod)

	def set_leading(self, leading: enums.LeadingExclPeriod) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:MODulation:EEPeriods:PUSCh:LEADing \n
		Snippet: driver.configure.multiEval.modulation.eePeriods.pusch.set_leading(leading = enums.LeadingExclPeriod.MS25) \n
		Specifies an EVM exclusion period at the beginning of a subframe (detected channel type 'PUSCH') . The specified period
		is excluded from the calculation of EVM, magnitude error and phase error results. \n
			:param leading: OFF | MS25 OFF: no exclusion MS25: 25 μs excluded
		"""
		param = Conversions.enum_scalar_to_str(leading, enums.LeadingExclPeriod)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:MODulation:EEPeriods:PUSCh:LEADing {param}')

	# noinspection PyTypeChecker
	def get_lagging(self) -> enums.LaggingExclPeriod:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:MODulation:EEPeriods:PUSCh:LAGGing \n
		Snippet: value: enums.LaggingExclPeriod = driver.configure.multiEval.modulation.eePeriods.pusch.get_lagging() \n
		Specifies an EVM exclusion period at the end of each subframe (detected channel type 'PUSCH') ; if SRS signals are
		allowed, at the end of each shortened subframe. The specified period is excluded from the calculation of EVM, magnitude
		error and phase error results. \n
			:return: lagging: OFF | MS05 | MS25 OFF: no exclusion MS05: 5 μs excluded MS25: 25 μs excluded
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:MEValuation:MODulation:EEPeriods:PUSCh:LAGGing?')
		return Conversions.str_to_scalar_enum(response, enums.LaggingExclPeriod)

	def set_lagging(self, lagging: enums.LaggingExclPeriod) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:MODulation:EEPeriods:PUSCh:LAGGing \n
		Snippet: driver.configure.multiEval.modulation.eePeriods.pusch.set_lagging(lagging = enums.LaggingExclPeriod.MS05) \n
		Specifies an EVM exclusion period at the end of each subframe (detected channel type 'PUSCH') ; if SRS signals are
		allowed, at the end of each shortened subframe. The specified period is excluded from the calculation of EVM, magnitude
		error and phase error results. \n
			:param lagging: OFF | MS05 | MS25 OFF: no exclusion MS05: 5 μs excluded MS25: 25 μs excluded
		"""
		param = Conversions.enum_scalar_to_str(lagging, enums.LaggingExclPeriod)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:MODulation:EEPeriods:PUSCh:LAGGing {param}')

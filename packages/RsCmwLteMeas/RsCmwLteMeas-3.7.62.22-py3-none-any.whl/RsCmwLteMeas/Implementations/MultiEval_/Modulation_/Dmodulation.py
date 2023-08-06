from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ....Internal.Types import DataType
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dmodulation:
	"""Dmodulation commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dmodulation", core, parent)

	# noinspection PyTypeChecker
	def fetch(self) -> enums.Modulation:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:MODulation:DMODulation \n
		Snippet: value: enums.Modulation = driver.multiEval.modulation.dmodulation.fetch() \n
		Returns the detected modulation scheme in the measured slot. If channel type PUCCH is detected, QPSK is returned as
		modulation type because the QPSK limits are applied in that case. \n
		Use RsCmwLteMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: modulation: QPSK | Q16 | Q64 | Q256 QPSK, 16-QAM, 64-QAM, 256-QAM"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:LTE:MEASurement<Instance>:MEValuation:MODulation:DMODulation?', suppressed)
		return Conversions.str_to_scalar_enum(response, enums.Modulation)

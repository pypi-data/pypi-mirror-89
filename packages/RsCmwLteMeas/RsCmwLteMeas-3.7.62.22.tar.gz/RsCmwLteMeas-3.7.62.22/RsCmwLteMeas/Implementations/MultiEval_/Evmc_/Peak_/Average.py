from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Average:
	"""Average commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("average", core, parent)

	def read(self) -> float:
		"""SCPI: READ:LTE:MEASurement<Instance>:MEValuation:EVMC:PEAK:AVERage \n
		Snippet: value: float = driver.multiEval.evmc.peak.average.read() \n
		The CURRent command returns the maximum value of the EVM vs subcarrier trace. The AVERage, MAXimum and SDEViation values
		are calculated from the CURRent values. The peak results cannot be displayed at the GUI. \n
		Use RsCmwLteMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: evm_cpeak_average: Unit: %"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'READ:LTE:MEASurement<Instance>:MEValuation:EVMC:PEAK:AVERage?', suppressed)
		return Conversions.str_to_float(response)

	def fetch(self) -> float:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:EVMC:PEAK:AVERage \n
		Snippet: value: float = driver.multiEval.evmc.peak.average.fetch() \n
		The CURRent command returns the maximum value of the EVM vs subcarrier trace. The AVERage, MAXimum and SDEViation values
		are calculated from the CURRent values. The peak results cannot be displayed at the GUI. \n
		Use RsCmwLteMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: evm_cpeak_average: Unit: %"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:LTE:MEASurement<Instance>:MEValuation:EVMC:PEAK:AVERage?', suppressed)
		return Conversions.str_to_float(response)

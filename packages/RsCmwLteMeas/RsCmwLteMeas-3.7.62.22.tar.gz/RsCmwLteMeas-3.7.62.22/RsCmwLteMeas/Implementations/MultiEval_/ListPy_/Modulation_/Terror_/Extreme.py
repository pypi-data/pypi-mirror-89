from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Extreme:
	"""Extreme commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("extreme", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:LIST:MODulation:TERRor:EXTReme \n
		Snippet: value: List[float] = driver.multiEval.listPy.modulation.terror.extreme.fetch() \n
		Return transmit time error values for all measured list mode segments. The values described below are returned by FETCh
		commands. CALCulate commands return limit check results instead, one value for each result listed below. \n
		Use RsCmwLteMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: timing_error: Comma-separated list of values, one per measured segment Unit: Ts (basic LTE time unit)"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:LTE:MEASurement<Instance>:MEValuation:LIST:MODulation:TERRor:EXTReme?', suppressed)
		return response

	def calculate(self) -> List[float]:
		"""SCPI: CALCulate:LTE:MEASurement<Instance>:MEValuation:LIST:MODulation:TERRor:EXTReme \n
		Snippet: value: List[float] = driver.multiEval.listPy.modulation.terror.extreme.calculate() \n
		Return transmit time error values for all measured list mode segments. The values described below are returned by FETCh
		commands. CALCulate commands return limit check results instead, one value for each result listed below. \n
		Use RsCmwLteMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: timing_error: Comma-separated list of values, one per measured segment Unit: Ts (basic LTE time unit)"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'CALCulate:LTE:MEASurement<Instance>:MEValuation:LIST:MODulation:TERRor:EXTReme?', suppressed)
		return response

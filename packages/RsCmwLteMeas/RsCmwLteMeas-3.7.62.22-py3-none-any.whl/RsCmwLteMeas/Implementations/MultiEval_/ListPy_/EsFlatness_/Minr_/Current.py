from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("current", core, parent)

	def fetch(self, minRange=repcap.MinRange.Default) -> List[float]:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:LIST:ESFLatness:MINR<nr>:CURRent \n
		Snippet: value: List[float] = driver.multiEval.listPy.esFlatness.minr.current.fetch(minRange = repcap.MinRange.Default) \n
		Return equalizer spectrum flatness single value results (minimum within a range) for all measured list mode segments. The
		values described below are returned by FETCh commands. CALCulate commands return limit check results instead, one value
		for each result listed below. \n
		Use RsCmwLteMeas.reliability.last_value to read the updated reliability indicator. \n
			:param minRange: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Minr')
			:return: min_r: Comma-separated list of values, one per measured segment Unit: dB"""
		minRange_cmd_val = self._base.get_repcap_cmd_value(minRange, repcap.MinRange)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:LTE:MEASurement<Instance>:MEValuation:LIST:ESFLatness:MINR{minRange_cmd_val}:CURRent?', suppressed)
		return response

	def calculate(self, minRange=repcap.MinRange.Default) -> List[float]:
		"""SCPI: CALCulate:LTE:MEASurement<Instance>:MEValuation:LIST:ESFLatness:MINR<nr>:CURRent \n
		Snippet: value: List[float] = driver.multiEval.listPy.esFlatness.minr.current.calculate(minRange = repcap.MinRange.Default) \n
		Return equalizer spectrum flatness single value results (minimum within a range) for all measured list mode segments. The
		values described below are returned by FETCh commands. CALCulate commands return limit check results instead, one value
		for each result listed below. \n
		Use RsCmwLteMeas.reliability.last_value to read the updated reliability indicator. \n
			:param minRange: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Minr')
			:return: min_r: Comma-separated list of values, one per measured segment Unit: dB"""
		minRange_cmd_val = self._base.get_repcap_cmd_value(minRange, repcap.MinRange)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'CALCulate:LTE:MEASurement<Instance>:MEValuation:LIST:ESFLatness:MINR{minRange_cmd_val}:CURRent?', suppressed)
		return response

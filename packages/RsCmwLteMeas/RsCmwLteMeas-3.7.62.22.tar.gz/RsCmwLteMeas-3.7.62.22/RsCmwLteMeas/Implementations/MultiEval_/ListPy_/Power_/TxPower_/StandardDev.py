from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StandardDev:
	"""StandardDev commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("standardDev", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:LIST:POWer:TXPower:SDEViation \n
		Snippet: value: List[float] = driver.multiEval.listPy.power.txPower.standardDev.fetch() \n
		Return the total TX power of all component carriers, for all measured list mode segments. \n
		Use RsCmwLteMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: tx_power: Comma-separated list of values, one per measured segment Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:LTE:MEASurement<Instance>:MEValuation:LIST:POWer:TXPower:SDEViation?', suppressed)
		return response

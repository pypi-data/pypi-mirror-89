from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Extreme:
	"""Extreme commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("extreme", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:LIST:IEMission:MARGin:EXTReme \n
		Snippet: value: List[float] = driver.multiEval.listPy.inbandEmission.margin.extreme.fetch() \n
		Return the inband emission limit line margin results for all measured list mode segments. The CURRent margins indicate
		the minimum (vertical) distance between the limit line and the current trace. A negative result indicates that the limit
		is exceeded. The AVERage, EXTReme and SDEViation values are calculated from the current margins. \n
		Use RsCmwLteMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: margin: Comma-separated list of values, one per measured segment Unit: dB"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:LTE:MEASurement<Instance>:MEValuation:LIST:IEMission:MARGin:EXTReme?', suppressed)
		return response

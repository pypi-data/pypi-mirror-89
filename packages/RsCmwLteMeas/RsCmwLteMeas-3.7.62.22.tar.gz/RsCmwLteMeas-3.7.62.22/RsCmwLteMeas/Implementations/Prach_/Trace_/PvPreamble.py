from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PvPreamble:
	"""PvPreamble commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pvPreamble", core, parent)

	def read(self) -> List[float]:
		"""SCPI: READ:LTE:MEASurement<Instance>:PRACh:TRACe:PVPReamble \n
		Snippet: value: List[float] = driver.prach.trace.pvPreamble.read() \n
		Return the values of the power vs. preamble traces. See also 'Views EVM vs Preamble, Power vs Preamble'. \n
		Use RsCmwLteMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: results: 32 power values, for preamble 1 to 32 (NCAP for not measured preambles) Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:LTE:MEASurement<Instance>:PRACh:TRACe:PVPReamble?', suppressed)
		return response

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:PRACh:TRACe:PVPReamble \n
		Snippet: value: List[float] = driver.prach.trace.pvPreamble.fetch() \n
		Return the values of the power vs. preamble traces. See also 'Views EVM vs Preamble, Power vs Preamble'. \n
		Use RsCmwLteMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: results: 32 power values, for preamble 1 to 32 (NCAP for not measured preambles) Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:LTE:MEASurement<Instance>:PRACh:TRACe:PVPReamble?', suppressed)
		return response

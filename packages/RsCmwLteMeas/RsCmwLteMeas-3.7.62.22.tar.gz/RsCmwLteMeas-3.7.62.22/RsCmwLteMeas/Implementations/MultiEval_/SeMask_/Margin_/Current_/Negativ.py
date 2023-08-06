from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Negativ:
	"""Negativ commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("negativ", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Out_Of_Tolerance: int: Out of tolerance result, i.e. percentage of measurement intervals of the statistic count for spectrum emission measurements exceeding the specified spectrum emission mask limits. Unit: %
			- Margin_Curr_Neg_X: List[float]: No parameter help available
			- Margin_Curr_Neg_Y: List[float]: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct('Margin_Curr_Neg_X', DataType.FloatList, None, False, True, 1),
			ArgStruct('Margin_Curr_Neg_Y', DataType.FloatList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tolerance: int = None
			self.Margin_Curr_Neg_X: List[float] = None
			self.Margin_Curr_Neg_Y: List[float] = None

	def fetch(self) -> FetchStruct:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:SEMask:MARGin:CURRent:NEGativ \n
		Snippet: value: FetchStruct = driver.multiEval.seMask.margin.current.negativ.fetch() \n
		Returns spectrum emission mask margin results. A negative margin indicates that the trace is located above the limit line,
		i.e. the limit is exceeded. The individual commands provide results for the CURRent, AVERage and maximum traces
		(resulting in MINimum margins) . For each trace, the X and Y values of the margins for emission mask areas 1 to 12 are
		provided for NEGative and POSitive offset frequencies. For inactive areas, NCAP is returned.
		Returned sequence: <Reliability>, <OutOfTolerance>, {<MarginX>, <MarginY>}area1, {...}area2, ..., {...}area12 \n
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		return self._core.io.query_struct(f'FETCh:LTE:MEASurement<Instance>:MEValuation:SEMask:MARGin:CURRent:NEGativ?', self.__class__.FetchStruct())

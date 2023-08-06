from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class High:
	"""High commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("high", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Iphase: List[float]: Normalized I amplitude
			- Qphase: List[float]: Normalized Q amplitude"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct('Iphase', DataType.FloatList, None, False, True, 1),
			ArgStruct('Qphase', DataType.FloatList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Iphase: List[float] = None
			self.Qphase: List[float] = None

	def fetch(self) -> FetchStruct:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:TRACe:IQ:HIGH \n
		Snippet: value: FetchStruct = driver.multiEval.trace.iq.high.fetch() \n
		Returns the results in the I/Q constellation diagram for low and high EVM window position. There is one pair of values
		per modulation symbol. The results are returned in the following order: <Reliability>, {<IPhase>, <QPhase>}symbol 1, ...,
		{<IPhase>, <QPhase>}symbol n See also 'View I/Q Constellation' \n
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		return self._core.io.query_struct(f'FETCh:LTE:MEASurement<Instance>:MEValuation:TRACe:IQ:HIGH?', self.__class__.FetchStruct())

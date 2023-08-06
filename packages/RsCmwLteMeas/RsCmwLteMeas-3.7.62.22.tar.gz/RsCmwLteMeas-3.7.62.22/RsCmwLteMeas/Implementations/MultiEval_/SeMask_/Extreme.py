from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Extreme:
	"""Extreme commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("extreme", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Out_Of_Tolerance: int: Out of tolerance result, i.e. percentage of measurement intervals of the statistic count for spectrum emission measurements exceeding the specified spectrum emission mask limits. Unit: %
			- Obw: float: Occupied bandwidth Unit: Hz
			- Tx_Power_Min: float: Minimum total TX power in the slot Unit: dBm
			- Tx_Power_Max: float: Maximum total TX power in the slot Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_float('Obw'),
			ArgStruct.scalar_float('Tx_Power_Min'),
			ArgStruct.scalar_float('Tx_Power_Max')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tolerance: int = None
			self.Obw: float = None
			self.Tx_Power_Min: float = None
			self.Tx_Power_Max: float = None

	def read(self) -> ResultData:
		"""SCPI: READ:LTE:MEASurement<Instance>:MEValuation:SEMask:EXTReme \n
		Snippet: value: ResultData = driver.multiEval.seMask.extreme.read() \n
		Return the extreme single value results of the spectrum emission measurement. The values described below are returned by
		FETCh and READ commands. CALCulate commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:LTE:MEASurement<Instance>:MEValuation:SEMask:EXTReme?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:SEMask:EXTReme \n
		Snippet: value: ResultData = driver.multiEval.seMask.extreme.fetch() \n
		Return the extreme single value results of the spectrum emission measurement. The values described below are returned by
		FETCh and READ commands. CALCulate commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:LTE:MEASurement<Instance>:MEValuation:SEMask:EXTReme?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Out_Of_Tolerance: int: Out of tolerance result, i.e. percentage of measurement intervals of the statistic count for spectrum emission measurements exceeding the specified spectrum emission mask limits. Unit: %
			- Obw: float: Occupied bandwidth Unit: Hz
			- Tx_Power_Min: float: Minimum total TX power in the slot Unit: dBm
			- Tx_Power_Max: float: Maximum total TX power in the slot Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_float('Obw'),
			ArgStruct.scalar_float('Tx_Power_Min'),
			ArgStruct.scalar_float('Tx_Power_Max')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tolerance: int = None
			self.Obw: float = None
			self.Tx_Power_Min: float = None
			self.Tx_Power_Max: float = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:LTE:MEASurement<Instance>:MEValuation:SEMask:EXTReme \n
		Snippet: value: CalculateStruct = driver.multiEval.seMask.extreme.calculate() \n
		Return the extreme single value results of the spectrum emission measurement. The values described below are returned by
		FETCh and READ commands. CALCulate commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:LTE:MEASurement<Instance>:MEValuation:SEMask:EXTReme?', self.__class__.CalculateStruct())

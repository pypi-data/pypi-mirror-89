from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("current", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Out_Of_Tolerance: int: Out of tolerance result, i.e. percentage of measurement intervals of the statistic count for power dynamics measurements exceeding the specified power dynamics limits. Unit: %
			- Off_Power_Before: float: No parameter help available
			- On_Power_Rms: float: No parameter help available
			- On_Power_Peak: float: No parameter help available
			- Off_Power_After: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_float('Off_Power_Before'),
			ArgStruct.scalar_float('On_Power_Rms'),
			ArgStruct.scalar_float('On_Power_Peak'),
			ArgStruct.scalar_float('Off_Power_After')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tolerance: int = None
			self.Off_Power_Before: float = None
			self.On_Power_Rms: float = None
			self.On_Power_Peak: float = None
			self.Off_Power_After: float = None

	def read(self) -> ResultData:
		"""SCPI: READ:LTE:MEASurement<Instance>:MEValuation:PDYNamics:CURRent \n
		Snippet: value: ResultData = driver.multiEval.pdynamics.current.read() \n
		Return the current, average, minimum, maximum and standard deviation single value results of the power dynamics
		measurement. A single result table row is returned, from left to right. The meaning of the values depends on the selected
		time mask, as follows:
			Table Header: Time mask / Power1 / Power2 / Power3 / Power4 \n
			- General on / off / OFF power (before) / ON power RMS / ON power peak / OFF power (after)
			- PUCCH / PUSCH / SRS / SRS ON / ON power RMS / ON power peak / ON power (after)
			- SRS blanking / SRS OFF / ON power RMS / ON power peak / ON power (after)
		The values described below are returned by FETCh and READ commands. CALCulate commands return limit check results instead,
		one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:LTE:MEASurement<Instance>:MEValuation:PDYNamics:CURRent?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:PDYNamics:CURRent \n
		Snippet: value: ResultData = driver.multiEval.pdynamics.current.fetch() \n
		Return the current, average, minimum, maximum and standard deviation single value results of the power dynamics
		measurement. A single result table row is returned, from left to right. The meaning of the values depends on the selected
		time mask, as follows:
			Table Header: Time mask / Power1 / Power2 / Power3 / Power4 \n
			- General on / off / OFF power (before) / ON power RMS / ON power peak / OFF power (after)
			- PUCCH / PUSCH / SRS / SRS ON / ON power RMS / ON power peak / ON power (after)
			- SRS blanking / SRS OFF / ON power RMS / ON power peak / ON power (after)
		The values described below are returned by FETCh and READ commands. CALCulate commands return limit check results instead,
		one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:LTE:MEASurement<Instance>:MEValuation:PDYNamics:CURRent?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Out_Of_Tolerance: int: Out of tolerance result, i.e. percentage of measurement intervals of the statistic count for power dynamics measurements exceeding the specified power dynamics limits. Unit: %
			- Off_Power_Before: float: No parameter help available
			- On_Power_Rms: float: No parameter help available
			- On_Power_Peak: float: No parameter help available
			- Off_Power_After: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_float('Off_Power_Before'),
			ArgStruct.scalar_float('On_Power_Rms'),
			ArgStruct.scalar_float('On_Power_Peak'),
			ArgStruct.scalar_float('Off_Power_After')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tolerance: int = None
			self.Off_Power_Before: float = None
			self.On_Power_Rms: float = None
			self.On_Power_Peak: float = None
			self.Off_Power_After: float = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:LTE:MEASurement<Instance>:MEValuation:PDYNamics:CURRent \n
		Snippet: value: CalculateStruct = driver.multiEval.pdynamics.current.calculate() \n
		Return the current, average, minimum, maximum and standard deviation single value results of the power dynamics
		measurement. A single result table row is returned, from left to right. The meaning of the values depends on the selected
		time mask, as follows:
			Table Header: Time mask / Power1 / Power2 / Power3 / Power4 \n
			- General on / off / OFF power (before) / ON power RMS / ON power peak / OFF power (after)
			- PUCCH / PUSCH / SRS / SRS ON / ON power RMS / ON power peak / ON power (after)
			- SRS blanking / SRS OFF / ON power RMS / ON power peak / ON power (after)
		The values described below are returned by FETCh and READ commands. CALCulate commands return limit check results instead,
		one value for each result listed below. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:LTE:MEASurement<Instance>:MEValuation:PDYNamics:CURRent?', self.__class__.CalculateStruct())

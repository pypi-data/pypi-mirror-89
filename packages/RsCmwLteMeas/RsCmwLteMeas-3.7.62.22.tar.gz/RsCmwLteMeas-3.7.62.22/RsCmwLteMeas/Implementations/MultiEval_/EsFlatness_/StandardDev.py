from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StandardDev:
	"""StandardDev commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("standardDev", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Out_Of_Tolerance: int: Out of tolerance result, i.e. percentage of measurement intervals of the statistic count for modulation measurements exceeding the specified equalizer spectrum flatness limits. Unit: %
			- Ripple_1: float: Max (range 1) - min (range 1) Unit: dB
			- Ripple_2: float: Max (range 2) - min (range 2) Unit: dB
			- Max_R_1_Min_R_2: float: Max (range 1) - min (range 2) Unit: dB
			- Max_R_2_Min_R_1: float: Max (range 2) - min (range 1) Unit: dB
			- Min_R_1: float: Min (range 1) Unit: dB
			- Max_R_1: float: Max (range 1) Unit: dB
			- Min_R_2: float: Min (range 2) Unit: dB
			- Max_R_2: float: Max (range 2) Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_float('Ripple_1'),
			ArgStruct.scalar_float('Ripple_2'),
			ArgStruct.scalar_float('Max_R_1_Min_R_2'),
			ArgStruct.scalar_float('Max_R_2_Min_R_1'),
			ArgStruct.scalar_float('Min_R_1'),
			ArgStruct.scalar_float('Max_R_1'),
			ArgStruct.scalar_float('Min_R_2'),
			ArgStruct.scalar_float('Max_R_2')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tolerance: int = None
			self.Ripple_1: float = None
			self.Ripple_2: float = None
			self.Max_R_1_Min_R_2: float = None
			self.Max_R_2_Min_R_1: float = None
			self.Min_R_1: float = None
			self.Max_R_1: float = None
			self.Min_R_2: float = None
			self.Max_R_2: float = None

	def read(self) -> ResultData:
		"""SCPI: READ:LTE:MEASurement<Instance>:MEValuation:ESFLatness:SDEViation \n
		Snippet: value: ResultData = driver.multiEval.esFlatness.standardDev.read() \n
		Return current, average, extreme and standard deviation single value results of the equalizer spectrum flatness
		measurement. See also 'Equalizer Spectrum Flatness Limits'. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:LTE:MEASurement<Instance>:MEValuation:ESFLatness:SDEViation?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:ESFLatness:SDEViation \n
		Snippet: value: ResultData = driver.multiEval.esFlatness.standardDev.fetch() \n
		Return current, average, extreme and standard deviation single value results of the equalizer spectrum flatness
		measurement. See also 'Equalizer Spectrum Flatness Limits'. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:LTE:MEASurement<Instance>:MEValuation:ESFLatness:SDEViation?', self.__class__.ResultData())

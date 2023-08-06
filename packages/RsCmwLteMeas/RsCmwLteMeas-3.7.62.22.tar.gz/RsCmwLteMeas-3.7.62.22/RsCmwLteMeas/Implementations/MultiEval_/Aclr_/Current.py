from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from .... import enums


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
			- Utra_2_Neg: float: ACLR for the second UTRA channel with lower frequency Unit: dB
			- Utra_1_Neg: float: ACLR for the first UTRA channel with lower frequency Unit: dB
			- Eutraneg: float: ACLR for the first E-UTRA channel with lower frequency Unit: dB
			- Eutra: float: Power in the allocated E-UTRA channel Unit: dBm
			- Eutrapos: float: ACLR for the first E-UTRA channel with higher frequency Unit: dB
			- Utra_1_Pos: float: ACLR for the first UTRA channel with higher frequency Unit: dB
			- Utra_2_Pos: float: ACLR for the second UTRA channel with higher frequency Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Utra_2_Neg'),
			ArgStruct.scalar_float('Utra_1_Neg'),
			ArgStruct.scalar_float('Eutraneg'),
			ArgStruct.scalar_float('Eutra'),
			ArgStruct.scalar_float('Eutrapos'),
			ArgStruct.scalar_float('Utra_1_Pos'),
			ArgStruct.scalar_float('Utra_2_Pos')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Utra_2_Neg: float = None
			self.Utra_1_Neg: float = None
			self.Eutraneg: float = None
			self.Eutra: float = None
			self.Eutrapos: float = None
			self.Utra_1_Pos: float = None
			self.Utra_2_Pos: float = None

	def read(self) -> ResultData:
		"""SCPI: READ:LTE:MEASurement<Instance>:MEValuation:ACLR:CURRent \n
		Snippet: value: ResultData = driver.multiEval.aclr.current.read() \n
		Returns the relative ACLR values as displayed in the table below the ACLR diagram. The current and average values can be
		retrieved. See also 'View Spectrum ACLR'. The values described below are returned by FETCh and READ commands. CALCulate
		commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:LTE:MEASurement<Instance>:MEValuation:ACLR:CURRent?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:ACLR:CURRent \n
		Snippet: value: ResultData = driver.multiEval.aclr.current.fetch() \n
		Returns the relative ACLR values as displayed in the table below the ACLR diagram. The current and average values can be
		retrieved. See also 'View Spectrum ACLR'. The values described below are returned by FETCh and READ commands. CALCulate
		commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:LTE:MEASurement<Instance>:MEValuation:ACLR:CURRent?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Utra_2_Neg: enums.ResultStatus2: ACLR for the second UTRA channel with lower frequency Unit: dB
			- Utra_1_Neg: enums.ResultStatus2: ACLR for the first UTRA channel with lower frequency Unit: dB
			- Eutraneg: enums.ResultStatus2: ACLR for the first E-UTRA channel with lower frequency Unit: dB
			- Eutra: enums.ResultStatus2: Power in the allocated E-UTRA channel Unit: dBm
			- Eutrapos: enums.ResultStatus2: ACLR for the first E-UTRA channel with higher frequency Unit: dB
			- Utra_1_Pos: enums.ResultStatus2: ACLR for the first UTRA channel with higher frequency Unit: dB
			- Utra_2_Pos: enums.ResultStatus2: ACLR for the second UTRA channel with higher frequency Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_enum('Utra_2_Neg', enums.ResultStatus2),
			ArgStruct.scalar_enum('Utra_1_Neg', enums.ResultStatus2),
			ArgStruct.scalar_enum('Eutraneg', enums.ResultStatus2),
			ArgStruct.scalar_enum('Eutra', enums.ResultStatus2),
			ArgStruct.scalar_enum('Eutrapos', enums.ResultStatus2),
			ArgStruct.scalar_enum('Utra_1_Pos', enums.ResultStatus2),
			ArgStruct.scalar_enum('Utra_2_Pos', enums.ResultStatus2)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Utra_2_Neg: enums.ResultStatus2 = None
			self.Utra_1_Neg: enums.ResultStatus2 = None
			self.Eutraneg: enums.ResultStatus2 = None
			self.Eutra: enums.ResultStatus2 = None
			self.Eutrapos: enums.ResultStatus2 = None
			self.Utra_1_Pos: enums.ResultStatus2 = None
			self.Utra_2_Pos: enums.ResultStatus2 = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:LTE:MEASurement<Instance>:MEValuation:ACLR:CURRent \n
		Snippet: value: CalculateStruct = driver.multiEval.aclr.current.calculate() \n
		Returns the relative ACLR values as displayed in the table below the ACLR diagram. The current and average values can be
		retrieved. See also 'View Spectrum ACLR'. The values described below are returned by FETCh and READ commands. CALCulate
		commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:LTE:MEASurement<Instance>:MEValuation:ACLR:CURRent?', self.__class__.CalculateStruct())

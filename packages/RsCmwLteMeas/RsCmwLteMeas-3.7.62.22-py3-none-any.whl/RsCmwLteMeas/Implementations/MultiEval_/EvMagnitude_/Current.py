from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("current", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Low: List[float]: EVM value for low EVM window position Unit: %
			- High: List[float]: EVM value for high EVM window position Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct('Low', DataType.FloatList, None, False, True, 1),
			ArgStruct('High', DataType.FloatList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Low: List[float] = None
			self.High: List[float] = None

	def read(self) -> ResultData:
		"""SCPI: READ:LTE:MEASurement<Instance>:MEValuation:EVMagnitude:CURRent \n
		Snippet: value: ResultData = driver.multiEval.evMagnitude.current.read() \n
		Returns the values of the EVM RMS bar graphs for the SC-FDMA symbols in the measured slot. The results of the current,
		average and maximum bar graphs can be retrieved. There is one pair of EVM values per SC-FDMA symbol, returned in the
		following order: <Reliability>, {<Low>, <High>}symbol 0, {<Low>, <High>}symbol 1, ... See also 'View Error Vector
		Magnitude'. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:LTE:MEASurement<Instance>:MEValuation:EVMagnitude:CURRent?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:EVMagnitude:CURRent \n
		Snippet: value: ResultData = driver.multiEval.evMagnitude.current.fetch() \n
		Returns the values of the EVM RMS bar graphs for the SC-FDMA symbols in the measured slot. The results of the current,
		average and maximum bar graphs can be retrieved. There is one pair of EVM values per SC-FDMA symbol, returned in the
		following order: <Reliability>, {<Low>, <High>}symbol 0, {<Low>, <High>}symbol 1, ... See also 'View Error Vector
		Magnitude'. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:LTE:MEASurement<Instance>:MEValuation:EVMagnitude:CURRent?', self.__class__.ResultData())

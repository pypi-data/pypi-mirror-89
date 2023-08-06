from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.StructBase import StructBase
from ...Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bler:
	"""Bler commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bler", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Ack: float: Received acknowledgments (percentage of sent scheduled subframes) Unit: %
			- Nack: float: Received negative acknowledgments (percentage of sent scheduled subframes) Unit: %
			- Bler: int: Block error ratio (percentage of sent scheduled subframes for which no ACK has been received) Unit: %
			- Dtx: float: Percentage of sent scheduled subframes for which no ACK and no NACK has been received Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Ack'),
			ArgStruct.scalar_float('Nack'),
			ArgStruct.scalar_int('Bler'),
			ArgStruct.scalar_float('Dtx')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Ack: float = None
			self.Nack: float = None
			self.Bler: int = None
			self.Dtx: float = None

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:BLER \n
		Snippet: value: ResultData = driver.multiEval.bler.fetch() \n
		Returns the block error ratio results determined from all captured subframes. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:LTE:MEASurement<Instance>:MEValuation:BLER?', self.__class__.ResultData())

	def read(self) -> ResultData:
		"""SCPI: READ:LTE:MEASurement<Instance>:MEValuation:BLER \n
		Snippet: value: ResultData = driver.multiEval.bler.read() \n
		Returns the block error ratio results determined from all captured subframes. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:LTE:MEASurement<Instance>:MEValuation:BLER?', self.__class__.ResultData())

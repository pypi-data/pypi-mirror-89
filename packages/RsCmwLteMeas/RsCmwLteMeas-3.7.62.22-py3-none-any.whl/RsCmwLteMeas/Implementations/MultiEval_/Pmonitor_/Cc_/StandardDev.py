from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import repcap


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
			- Out_Of_Tolerance: int: Out of tolerance result, i.e. percentage of measurement intervals of the statistic count that exceed the specified limits Unit: %
			- Tx_Power: float: Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_float('Tx_Power')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tolerance: int = None
			self.Tx_Power: float = None

	def read(self, carrierComponent=repcap.CarrierComponent.Default) -> ResultData:
		"""SCPI: READ:LTE:MEASurement<Instance>:MEValuation:PMONitor:CC<Nr>:SDEViation \n
		Snippet: value: ResultData = driver.multiEval.pmonitor.cc.standardDev.read(carrierComponent = repcap.CarrierComponent.Default) \n
		Returns the TX power of carrier CC<no>. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: structure: for return value, see the help for ResultData structure arguments."""
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		return self._core.io.query_struct(f'READ:LTE:MEASurement<Instance>:MEValuation:PMONitor:CC{carrierComponent_cmd_val}:SDEViation?', self.__class__.ResultData())

	def fetch(self, carrierComponent=repcap.CarrierComponent.Default) -> ResultData:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:PMONitor:CC<Nr>:SDEViation \n
		Snippet: value: ResultData = driver.multiEval.pmonitor.cc.standardDev.fetch(carrierComponent = repcap.CarrierComponent.Default) \n
		Returns the TX power of carrier CC<no>. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: structure: for return value, see the help for ResultData structure arguments."""
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		return self._core.io.query_struct(f'FETCh:LTE:MEASurement<Instance>:MEValuation:PMONitor:CC{carrierComponent_cmd_val}:SDEViation?', self.__class__.ResultData())

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RbIndex:
	"""RbIndex commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rbIndex", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Out_Of_Tolerance: int: Out of tolerance result, i.e. percentage of measurement intervals of the statistic count for modulation measurements exceeding the specified inband emission limits. Unit: %
			- Rb_Index: int: Resource block index"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_int('Rb_Index')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tolerance: int = None
			self.Rb_Index: int = None

	def fetch(self, carrierComponent=repcap.CarrierComponent.Default) -> FetchStruct:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:IEMission:CC<Nr>:MARGin:CURRent:RBINdex \n
		Snippet: value: FetchStruct = driver.multiEval.inbandEmission.cc.margin.current.rbIndex.fetch(carrierComponent = repcap.CarrierComponent.Default) \n
		Return resource block indices for CC<no> inband emission margins. At these RB indices, the CURRent and EXTReme margins
		have been detected (see method RsCmwLteMeas.MultiEval.InbandEmission.Cc.Margin.Current.fetch and ...:EXTReme) . \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		return self._core.io.query_struct(f'FETCh:LTE:MEASurement<Instance>:MEValuation:IEMission:CC{carrierComponent_cmd_val}:MARGin:CURRent:RBINdex?', self.__class__.FetchStruct())

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Extreme:
	"""Extreme commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("extreme", core, parent)

	@property
	def rbIndex(self):
		"""rbIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbIndex'):
			from .Extreme_.RbIndex import RbIndex
			self._rbIndex = RbIndex(self._core, self._base)
		return self._rbIndex

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Out_Of_Tolerance: int: Out of tolerance result, i.e. percentage of measurement intervals of the statistic count for modulation measurements exceeding the specified inband emission limits. Unit: %
			- Margin: float: Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_float('Margin')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tolerance: int = None
			self.Margin: float = None

	def fetch(self, carrierComponent=repcap.CarrierComponent.Default) -> FetchStruct:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:IEMission:CC<Nr>:MARGin:EXTReme \n
		Snippet: value: FetchStruct = driver.multiEval.inbandEmission.cc.margin.extreme.fetch(carrierComponent = repcap.CarrierComponent.Default) \n
		Return the limit line margin results for the CC<no> diagram. The CURRent margin indicates the minimum (vertical) distance
		between the inband emissions limit line and the current trace. A negative result indicates that the limit is exceeded.
		The AVERage, EXTReme and SDEViation values are calculated from the current margins. The margin results cannot be
		displayed at the GUI. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		return self._core.io.query_struct(f'FETCh:LTE:MEASurement<Instance>:MEValuation:IEMission:CC{carrierComponent_cmd_val}:MARGin:EXTReme?', self.__class__.FetchStruct())

	def clone(self) -> 'Extreme':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Extreme(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

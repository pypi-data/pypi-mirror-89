from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.StructBase import StructBase
from .........Internal.ArgStruct import ArgStruct
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ChannelBw2nd:
	"""ChannelBw2nd commands group definition. 2 total commands, 1 Sub-groups, 1 group commands
	Repeated Capability: SecondChannelBw, default value after init: SecondChannelBw.Bw50"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("channelBw2nd", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_secondChannelBw_get', 'repcap_secondChannelBw_set', repcap.SecondChannelBw.Bw50)

	def repcap_secondChannelBw_set(self, enum_value: repcap.SecondChannelBw) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to SecondChannelBw.Default
		Default value after init: SecondChannelBw.Bw50"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_secondChannelBw_get(self) -> repcap.SecondChannelBw:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def channelBw3rd(self):
		"""channelBw3rd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_channelBw3rd'):
			from .ChannelBw2nd_.ChannelBw3rd import ChannelBw3rd
			self._channelBw3rd = ChannelBw3rd(self._core, self._base)
		return self._channelBw3rd

	# noinspection PyTypeChecker
	class ChannelBw2ndStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Enable: bool: OFF | ON OFF: disables the check of these requirements ON: enables the check of these requirements
			- Frequency_Start: float: Start frequency of the area, relative to the edges of the aggregated channel bandwidth Range: 0 MHz to 65 MHz, Unit: Hz
			- Frequency_End: float: Stop frequency of the area, relative to the edges of the aggregated channel bandwidth Range: 0 MHz to 65 MHz, Unit: Hz
			- Level: float: Upper limit for the area Range: -256 dBm to 256 dBm, Unit: dBm
			- Rbw: enums.Rbw: K030 | K100 | M1 Resolution bandwidth to be used for the area K030: 30 kHz K100: 100 kHz M1: 1 MHz"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Frequency_Start'),
			ArgStruct.scalar_float('Frequency_End'),
			ArgStruct.scalar_float('Level'),
			ArgStruct.scalar_enum('Rbw', enums.Rbw)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Frequency_Start: float = None
			self.Frequency_End: float = None
			self.Level: float = None
			self.Rbw: enums.Rbw = None

	def set(self, structure: ChannelBw2ndStruct, limit=repcap.Limit.Default, firstChannelBw=repcap.FirstChannelBw.Default, secondChannelBw=repcap.SecondChannelBw.Default) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:LIMit:SEMask:LIMit<nr>:CAGGregation:CBANdwidth<Band1>:CBANdwidth<Band2> \n
		Snippet: driver.configure.multiEval.limit.seMask.limit.carrierAggregation.channelBw1st.channelBw2nd.set(value = [PROPERTY_STRUCT_NAME](), limit = repcap.Limit.Default, firstChannelBw = repcap.FirstChannelBw.Default, secondChannelBw = repcap.SecondChannelBw.Default) \n
		Defines general requirements for the emission mask area <no>. The activation state, the area borders, an upper limit and
		the resolution bandwidth must be specified. The settings are defined separately for each channel bandwidth combination,
		for two aggregated carriers. The following bandwidth combinations are supported: Example: For the first line in the
		figure, use ...:CBANdwidth200:CBANdwidth50. \n
			:param structure: for set value, see the help for ChannelBw2ndStruct structure arguments.
			:param limit: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Limit')
			:param firstChannelBw: optional repeated capability selector. Default value: Bw150 (settable in the interface 'ChannelBw1st')
			:param secondChannelBw: optional repeated capability selector. Default value: Bw50 (settable in the interface 'ChannelBw2nd')"""
		limit_cmd_val = self._base.get_repcap_cmd_value(limit, repcap.Limit)
		firstChannelBw_cmd_val = self._base.get_repcap_cmd_value(firstChannelBw, repcap.FirstChannelBw)
		secondChannelBw_cmd_val = self._base.get_repcap_cmd_value(secondChannelBw, repcap.SecondChannelBw)
		self._core.io.write_struct(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:LIMit:SEMask:LIMit{limit_cmd_val}:CAGGregation:CBANdwidth{firstChannelBw_cmd_val}:CBANdwidth{secondChannelBw_cmd_val}', structure)

	def get(self, limit=repcap.Limit.Default, firstChannelBw=repcap.FirstChannelBw.Default, secondChannelBw=repcap.SecondChannelBw.Default) -> ChannelBw2ndStruct:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:LIMit:SEMask:LIMit<nr>:CAGGregation:CBANdwidth<Band1>:CBANdwidth<Band2> \n
		Snippet: value: ChannelBw2ndStruct = driver.configure.multiEval.limit.seMask.limit.carrierAggregation.channelBw1st.channelBw2nd.get(limit = repcap.Limit.Default, firstChannelBw = repcap.FirstChannelBw.Default, secondChannelBw = repcap.SecondChannelBw.Default) \n
		Defines general requirements for the emission mask area <no>. The activation state, the area borders, an upper limit and
		the resolution bandwidth must be specified. The settings are defined separately for each channel bandwidth combination,
		for two aggregated carriers. The following bandwidth combinations are supported: Example: For the first line in the
		figure, use ...:CBANdwidth200:CBANdwidth50. \n
			:param limit: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Limit')
			:param firstChannelBw: optional repeated capability selector. Default value: Bw150 (settable in the interface 'ChannelBw1st')
			:param secondChannelBw: optional repeated capability selector. Default value: Bw50 (settable in the interface 'ChannelBw2nd')
			:return: structure: for return value, see the help for ChannelBw2ndStruct structure arguments."""
		limit_cmd_val = self._base.get_repcap_cmd_value(limit, repcap.Limit)
		firstChannelBw_cmd_val = self._base.get_repcap_cmd_value(firstChannelBw, repcap.FirstChannelBw)
		secondChannelBw_cmd_val = self._base.get_repcap_cmd_value(secondChannelBw, repcap.SecondChannelBw)
		return self._core.io.query_struct(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:LIMit:SEMask:LIMit{limit_cmd_val}:CAGGregation:CBANdwidth{firstChannelBw_cmd_val}:CBANdwidth{secondChannelBw_cmd_val}?', self.__class__.ChannelBw2ndStruct())

	def clone(self) -> 'ChannelBw2nd':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ChannelBw2nd(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

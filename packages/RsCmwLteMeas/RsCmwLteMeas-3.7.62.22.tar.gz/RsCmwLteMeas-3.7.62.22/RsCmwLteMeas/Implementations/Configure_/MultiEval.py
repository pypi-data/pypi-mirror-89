from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.StructBase import StructBase
from ...Internal.ArgStruct import ArgStruct
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MultiEval:
	"""MultiEval commands group definition. 133 total commands, 15 Sub-groups, 19 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("multiEval", core, parent)

	@property
	def listPy(self):
		"""listPy commands group. 2 Sub-classes, 3 commands."""
		if not hasattr(self, '_listPy'):
			from .MultiEval_.ListPy import ListPy
			self._listPy = ListPy(self._core, self._base)
		return self._listPy

	@property
	def tmode(self):
		"""tmode commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_tmode'):
			from .MultiEval_.Tmode import Tmode
			self._tmode = Tmode(self._core, self._base)
		return self._tmode

	@property
	def pcc(self):
		"""pcc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pcc'):
			from .MultiEval_.Pcc import Pcc
			self._pcc = Pcc(self._core, self._base)
		return self._pcc

	@property
	def cc(self):
		"""cc commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_cc'):
			from .MultiEval_.Cc import Cc
			self._cc = Cc(self._core, self._base)
		return self._cc

	@property
	def nsvalue(self):
		"""nsvalue commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_nsvalue'):
			from .MultiEval_.Nsvalue import Nsvalue
			self._nsvalue = Nsvalue(self._core, self._base)
		return self._nsvalue

	@property
	def srs(self):
		"""srs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_srs'):
			from .MultiEval_.Srs import Srs
			self._srs = Srs(self._core, self._base)
		return self._srs

	@property
	def modulation(self):
		"""modulation commands group. 3 Sub-classes, 3 commands."""
		if not hasattr(self, '_modulation'):
			from .MultiEval_.Modulation import Modulation
			self._modulation = Modulation(self._core, self._base)
		return self._modulation

	@property
	def spectrum(self):
		"""spectrum commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_spectrum'):
			from .MultiEval_.Spectrum import Spectrum
			self._spectrum = Spectrum(self._core, self._base)
		return self._spectrum

	@property
	def rbAllocation(self):
		"""rbAllocation commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbAllocation'):
			from .MultiEval_.RbAllocation import RbAllocation
			self._rbAllocation = RbAllocation(self._core, self._base)
		return self._rbAllocation

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .MultiEval_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def pdynamics(self):
		"""pdynamics commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_pdynamics'):
			from .MultiEval_.Pdynamics import Pdynamics
			self._pdynamics = Pdynamics(self._core, self._base)
		return self._pdynamics

	@property
	def scount(self):
		"""scount commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_scount'):
			from .MultiEval_.Scount import Scount
			self._scount = Scount(self._core, self._base)
		return self._scount

	@property
	def result(self):
		"""result commands group. 1 Sub-classes, 14 commands."""
		if not hasattr(self, '_result'):
			from .MultiEval_.Result import Result
			self._result = Result(self._core, self._base)
		return self._result

	@property
	def limit(self):
		"""limit commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_limit'):
			from .MultiEval_.Limit import Limit
			self._limit = Limit(self._core, self._base)
		return self._limit

	@property
	def bler(self):
		"""bler commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bler'):
			from .MultiEval_.Bler import Bler
			self._bler = Bler(self._core, self._base)
		return self._bler

	def get_timeout(self) -> float:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:TOUT \n
		Snippet: value: float = driver.configure.multiEval.get_timeout() \n
		Defines a timeout for the measurement. The timer is started when the measurement is initiated via a READ or INIT command.
		It is not started if the measurement is initiated manually ([ON | OFF] key or [RESTART | STOP] key) .
		When the measurement has completed the first measurement cycle (first single shot) , the statistical depth is reached and
		the timer is reset. If the first measurement cycle has not been completed when the timer expires, the measurement is
		stopped. The measurement state changes to RDY. The reliability indicator is set to 1, indicating that a measurement
		timeout occurred. Still running READ, FETCh or CALCulate commands are completed, returning the available results.
		At least for some results, there are no values at all or the statistical depth has not been reached. A timeout of 0 s
		corresponds to an infinite measurement timeout. \n
			:return: timeout: Unit: s
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:MEValuation:TOUT?')
		return Conversions.str_to_float(response)

	def set_timeout(self, timeout: float) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:TOUT \n
		Snippet: driver.configure.multiEval.set_timeout(timeout = 1.0) \n
		Defines a timeout for the measurement. The timer is started when the measurement is initiated via a READ or INIT command.
		It is not started if the measurement is initiated manually ([ON | OFF] key or [RESTART | STOP] key) .
		When the measurement has completed the first measurement cycle (first single shot) , the statistical depth is reached and
		the timer is reset. If the first measurement cycle has not been completed when the timer expires, the measurement is
		stopped. The measurement state changes to RDY. The reliability indicator is set to 1, indicating that a measurement
		timeout occurred. Still running READ, FETCh or CALCulate commands are completed, returning the available results.
		At least for some results, there are no values at all or the statistical depth has not been reached. A timeout of 0 s
		corresponds to an infinite measurement timeout. \n
			:param timeout: Unit: s
		"""
		param = Conversions.decimal_value_to_str(timeout)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:TOUT {param}')

	# noinspection PyTypeChecker
	def get_mmode(self) -> enums.MeasurementMode:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:MMODe \n
		Snippet: value: enums.MeasurementMode = driver.configure.multiEval.get_mmode() \n
		Selects the measurement mode. \n
			:return: measurement_mode: NORMal | TMODe | MELMode NORMal: normal mode TMODe: TPC mode MELMode: multi-evaluation list mode
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:MEValuation:MMODe?')
		return Conversions.str_to_scalar_enum(response, enums.MeasurementMode)

	def set_mmode(self, measurement_mode: enums.MeasurementMode) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:MMODe \n
		Snippet: driver.configure.multiEval.set_mmode(measurement_mode = enums.MeasurementMode.MELMode) \n
		Selects the measurement mode. \n
			:param measurement_mode: NORMal | TMODe | MELMode NORMal: normal mode TMODe: TPC mode MELMode: multi-evaluation list mode
		"""
		param = Conversions.enum_scalar_to_str(measurement_mode, enums.MeasurementMode)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:MMODe {param}')

	# noinspection PyTypeChecker
	def get_repetition(self) -> enums.Repeat:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:REPetition \n
		Snippet: value: enums.Repeat = driver.configure.multiEval.get_repetition() \n
		Specifies the repetition mode of the measurement. The repetition mode specifies whether the measurement is stopped after
		a single shot or repeated continuously. Use CONFigure:..:MEAS<i>:...:SCOunt to determine the number of measurement
		intervals per single shot. \n
			:return: repetition: SINGleshot | CONTinuous SINGleshot: Single-shot measurement CONTinuous: Continuous measurement
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:MEValuation:REPetition?')
		return Conversions.str_to_scalar_enum(response, enums.Repeat)

	def set_repetition(self, repetition: enums.Repeat) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:REPetition \n
		Snippet: driver.configure.multiEval.set_repetition(repetition = enums.Repeat.CONTinuous) \n
		Specifies the repetition mode of the measurement. The repetition mode specifies whether the measurement is stopped after
		a single shot or repeated continuously. Use CONFigure:..:MEAS<i>:...:SCOunt to determine the number of measurement
		intervals per single shot. \n
			:param repetition: SINGleshot | CONTinuous SINGleshot: Single-shot measurement CONTinuous: Continuous measurement
		"""
		param = Conversions.enum_scalar_to_str(repetition, enums.Repeat)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:REPetition {param}')

	# noinspection PyTypeChecker
	def get_scondition(self) -> enums.StopCondition:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:SCONdition \n
		Snippet: value: enums.StopCondition = driver.configure.multiEval.get_scondition() \n
		Qualifies whether the measurement is stopped after a failed limit check or continued. SLFail means that the measurement
		is stopped and reaches the RDY state when one of the results exceeds the limits. \n
			:return: stop_condition: NONE | SLFail NONE: Continue measurement irrespective of the limit check SLFail: Stop measurement on limit failure
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:MEValuation:SCONdition?')
		return Conversions.str_to_scalar_enum(response, enums.StopCondition)

	def set_scondition(self, stop_condition: enums.StopCondition) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:SCONdition \n
		Snippet: driver.configure.multiEval.set_scondition(stop_condition = enums.StopCondition.NONE) \n
		Qualifies whether the measurement is stopped after a failed limit check or continued. SLFail means that the measurement
		is stopped and reaches the RDY state when one of the results exceeds the limits. \n
			:param stop_condition: NONE | SLFail NONE: Continue measurement irrespective of the limit check SLFail: Stop measurement on limit failure
		"""
		param = Conversions.enum_scalar_to_str(stop_condition, enums.StopCondition)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:SCONdition {param}')

	def get_ul_dl(self) -> int:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:ULDL \n
		Snippet: value: int = driver.configure.multiEval.get_ul_dl() \n
		Selects an UL-DL configuration, defining the combination of uplink, downlink and special subframes within a radio frame.
		This parameter is only relevant for frame structure 'Type 2' (method RsCmwLteMeas.Configure.fstructure) .
		The UL-DL configurations are defined in 3GPP TS 36.211, chapter 4, 'Frame Structure'.
			INTRO_CMD_HELP: For the combined signal path scenario, use: \n
			- CONFigure:LTE:SIGN<i>:ULDL
			- CONFigure:LTE:SIGN<i>:CELL:SCC<c>:ULDL
			- CONFigure:LTE:SIGN<i>:CELL:TDD:SPECific \n
			:return: uplink_downlink: Range: 0 to 6
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:MEValuation:ULDL?')
		return Conversions.str_to_int(response)

	def set_ul_dl(self, uplink_downlink: int) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:ULDL \n
		Snippet: driver.configure.multiEval.set_ul_dl(uplink_downlink = 1) \n
		Selects an UL-DL configuration, defining the combination of uplink, downlink and special subframes within a radio frame.
		This parameter is only relevant for frame structure 'Type 2' (method RsCmwLteMeas.Configure.fstructure) .
		The UL-DL configurations are defined in 3GPP TS 36.211, chapter 4, 'Frame Structure'.
			INTRO_CMD_HELP: For the combined signal path scenario, use: \n
			- CONFigure:LTE:SIGN<i>:ULDL
			- CONFigure:LTE:SIGN<i>:CELL:SCC<c>:ULDL
			- CONFigure:LTE:SIGN<i>:CELL:TDD:SPECific \n
			:param uplink_downlink: Range: 0 to 6
		"""
		param = Conversions.decimal_value_to_str(uplink_downlink)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:ULDL {param}')

	def get_ssubframe(self) -> int:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:SSUBframe \n
		Snippet: value: int = driver.configure.multiEval.get_ssubframe() \n
		Selects a special subframe configuration, defining the inner structure of special subframes. This parameter is only
		relevant for frame structure 'Type 2' (method RsCmwLteMeas.Configure.fstructure) . The special subframe configurations
		are defined in 3GPP TS 36.211, chapter 4, 'Frame Structure'.
			INTRO_CMD_HELP: For the combined signal path scenario, use: \n
			- CONFigure:LTE:SIGN<i>:SSUBframe
			- CONFigure:LTE:SIGN<i>:CELL:SCC<c>:SSUBframe
			- CONFigure:LTE:SIGN<i>:CELL:TDD:SPECific \n
			:return: special_subframe: Range: 0 to 8
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:MEValuation:SSUBframe?')
		return Conversions.str_to_int(response)

	def set_ssubframe(self, special_subframe: int) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:SSUBframe \n
		Snippet: driver.configure.multiEval.set_ssubframe(special_subframe = 1) \n
		Selects a special subframe configuration, defining the inner structure of special subframes. This parameter is only
		relevant for frame structure 'Type 2' (method RsCmwLteMeas.Configure.fstructure) . The special subframe configurations
		are defined in 3GPP TS 36.211, chapter 4, 'Frame Structure'.
			INTRO_CMD_HELP: For the combined signal path scenario, use: \n
			- CONFigure:LTE:SIGN<i>:SSUBframe
			- CONFigure:LTE:SIGN<i>:CELL:SCC<c>:SSUBframe
			- CONFigure:LTE:SIGN<i>:CELL:TDD:SPECific \n
			:param special_subframe: Range: 0 to 8
		"""
		param = Conversions.decimal_value_to_str(special_subframe)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:SSUBframe {param}')

	def get_mo_exception(self) -> bool:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:MOEXception \n
		Snippet: value: bool = driver.configure.multiEval.get_mo_exception() \n
		Specifies whether measurement results that the R&S CMW identifies as faulty or inaccurate are rejected. \n
			:return: meas_on_exception: OFF | ON OFF: Faulty results are rejected ON: Results are never rejected
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:MEValuation:MOEXception?')
		return Conversions.str_to_bool(response)

	def set_mo_exception(self, meas_on_exception: bool) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:MOEXception \n
		Snippet: driver.configure.multiEval.set_mo_exception(meas_on_exception = False) \n
		Specifies whether measurement results that the R&S CMW identifies as faulty or inaccurate are rejected. \n
			:param meas_on_exception: OFF | ON OFF: Faulty results are rejected ON: Results are never rejected
		"""
		param = Conversions.bool_to_str(meas_on_exception)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:MOEXception {param}')

	# noinspection PyTypeChecker
	def get_cprefix(self) -> enums.CyclicPrefix:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:CPRefix \n
		Snippet: value: enums.CyclicPrefix = driver.configure.multiEval.get_cprefix() \n
		Selects the type of cyclic prefix of the LTE signal. For the combined signal path scenario,
		useCONFigure:LTE:SIGN<i>:CELL:CPRefix. \n
			:return: cyclic_prefix: NORMal | EXTended
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:MEValuation:CPRefix?')
		return Conversions.str_to_scalar_enum(response, enums.CyclicPrefix)

	def set_cprefix(self, cyclic_prefix: enums.CyclicPrefix) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:CPRefix \n
		Snippet: driver.configure.multiEval.set_cprefix(cyclic_prefix = enums.CyclicPrefix.EXTended) \n
		Selects the type of cyclic prefix of the LTE signal. For the combined signal path scenario,
		useCONFigure:LTE:SIGN<i>:CELL:CPRefix. \n
			:param cyclic_prefix: NORMal | EXTended
		"""
		param = Conversions.enum_scalar_to_str(cyclic_prefix, enums.CyclicPrefix)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:CPRefix {param}')

	# noinspection PyTypeChecker
	def get_ctype(self) -> enums.ChannelTypeDetection:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:CTYPe \n
		Snippet: value: enums.ChannelTypeDetection = driver.configure.multiEval.get_ctype() \n
		Configures the channel type detection for uplink measurements. \n
			:return: channel_type: AUTO | PUSCh | PUCCh Automatic detection of channel type or manual selection
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:MEValuation:CTYPe?')
		return Conversions.str_to_scalar_enum(response, enums.ChannelTypeDetection)

	def set_ctype(self, channel_type: enums.ChannelTypeDetection) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:CTYPe \n
		Snippet: driver.configure.multiEval.set_ctype(channel_type = enums.ChannelTypeDetection.AUTO) \n
		Configures the channel type detection for uplink measurements. \n
			:param channel_type: AUTO | PUSCh | PUCCh Automatic detection of channel type or manual selection
		"""
		param = Conversions.enum_scalar_to_str(channel_type, enums.ChannelTypeDetection)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:CTYPe {param}')

	# noinspection PyTypeChecker
	def get_sctype(self) -> enums.SidelinkChannelType:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:SCTYpe \n
		Snippet: value: enums.SidelinkChannelType = driver.configure.multiEval.get_sctype() \n
		Configures the channel type for modulation results of sidelink measurements. \n
			:return: channel_type: PSSCh | PSCCh
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:MEValuation:SCTYpe?')
		return Conversions.str_to_scalar_enum(response, enums.SidelinkChannelType)

	def set_sctype(self, channel_type: enums.SidelinkChannelType) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:SCTYpe \n
		Snippet: driver.configure.multiEval.set_sctype(channel_type = enums.SidelinkChannelType.PSCCh) \n
		Configures the channel type for modulation results of sidelink measurements. \n
			:param channel_type: PSSCh | PSCCh
		"""
		param = Conversions.enum_scalar_to_str(channel_type, enums.SidelinkChannelType)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:SCTYpe {param}')

	def get_peak_search(self) -> bool:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:PSEarch \n
		Snippet: value: bool = driver.configure.multiEval.get_peak_search() \n
		No command help available \n
			:return: pucch_search: No help available
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:MEValuation:PSEarch?')
		return Conversions.str_to_bool(response)

	def set_peak_search(self, pucch_search: bool) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:PSEarch \n
		Snippet: driver.configure.multiEval.set_peak_search(pucch_search = False) \n
		No command help available \n
			:param pucch_search: No help available
		"""
		param = Conversions.bool_to_str(pucch_search)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:PSEarch {param}')

	# noinspection PyTypeChecker
	def get_pformat(self) -> enums.PucchFormat:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:PFORmat \n
		Snippet: value: enums.PucchFormat = driver.configure.multiEval.get_pformat() \n
		Specifies the PUCCH format (only relevant for signals containing a PUCCH) . The formats are defined in 3GPP TS 36.211. \n
			:return: pucch_format: F1 | F1A | F1B | F2 | F2A | F2B | F3
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:MEValuation:PFORmat?')
		return Conversions.str_to_scalar_enum(response, enums.PucchFormat)

	def set_pformat(self, pucch_format: enums.PucchFormat) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:PFORmat \n
		Snippet: driver.configure.multiEval.set_pformat(pucch_format = enums.PucchFormat.F1) \n
		Specifies the PUCCH format (only relevant for signals containing a PUCCH) . The formats are defined in 3GPP TS 36.211. \n
			:param pucch_format: F1 | F1A | F1B | F2 | F2A | F2B | F3
		"""
		param = Conversions.enum_scalar_to_str(pucch_format, enums.PucchFormat)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:PFORmat {param}')

	def get_nvfilter(self) -> int or bool:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:NVFilter \n
		Snippet: value: int or bool = driver.configure.multiEval.get_nvfilter() \n
		Specifies, enables or disables the number of resource blocks (NRB) view filter. If the filter is active, only slots with
		a matching number of allocated resource blocks are measured. Within the indicated input range, only specific numbers are
		allowed as defined in 3GPP TS 36.211. For details, see 'Resources in Time and Frequency Domain'. \n
			:return: nrb_view_filter: Number of allocated resource blocks Range: 1 to 100 Additional parameters: OFF | ON (disables | enables the filter)
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:MEValuation:NVFilter?')
		return Conversions.str_to_int_or_bool(response)

	def set_nvfilter(self, nrb_view_filter: int or bool) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:NVFilter \n
		Snippet: driver.configure.multiEval.set_nvfilter(nrb_view_filter = 1) \n
		Specifies, enables or disables the number of resource blocks (NRB) view filter. If the filter is active, only slots with
		a matching number of allocated resource blocks are measured. Within the indicated input range, only specific numbers are
		allowed as defined in 3GPP TS 36.211. For details, see 'Resources in Time and Frequency Domain'. \n
			:param nrb_view_filter: Number of allocated resource blocks Range: 1 to 100 Additional parameters: OFF | ON (disables | enables the filter)
		"""
		param = Conversions.decimal_or_bool_value_to_str(nrb_view_filter)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:NVFilter {param}')

	def get_orv_filter(self) -> int or bool:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:ORVFilter \n
		Snippet: value: int or bool = driver.configure.multiEval.get_orv_filter() \n
		Specifies, enables or disables the RB offset view filter. If the filter is active, only slots with a matching number of
		RB offset are measured. The indicated input range applies to a 20-MHz channel bandwidth. The maximum value depends on the
		bandwidth (maximum number of RBs minus one) . \n
			:return: offset_rb: Offset of the first allocated RB Range: 0 to 99 Additional parameters: OFF | ON (disables | enables the filter)
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:MEValuation:ORVFilter?')
		return Conversions.str_to_int_or_bool(response)

	def set_orv_filter(self, offset_rb: int or bool) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:ORVFilter \n
		Snippet: driver.configure.multiEval.set_orv_filter(offset_rb = 1) \n
		Specifies, enables or disables the RB offset view filter. If the filter is active, only slots with a matching number of
		RB offset are measured. The indicated input range applies to a 20-MHz channel bandwidth. The maximum value depends on the
		bandwidth (maximum number of RBs minus one) . \n
			:param offset_rb: Offset of the first allocated RB Range: 0 to 99 Additional parameters: OFF | ON (disables | enables the filter)
		"""
		param = Conversions.decimal_or_bool_value_to_str(offset_rb)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:ORVFilter {param}')

	# noinspection PyTypeChecker
	def get_ctv_filter(self) -> enums.ChannelTypeVewFilter:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:CTVFilter \n
		Snippet: value: enums.ChannelTypeVewFilter = driver.configure.multiEval.get_ctv_filter() \n
		Specifies, enables or disables the channel type view filter. If the filter is active, only slots with detected channel
		type PUSCH or PUCCH are measured. \n
			:return: channel_type: PUSCh | PUCCh | ON | OFF PUSCh: measure only physical uplink shared channel PUCCh: measure only physical uplink control channel ON: enable the filter OFF: disable the filter
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:MEValuation:CTVFilter?')
		return Conversions.str_to_scalar_enum(response, enums.ChannelTypeVewFilter)

	def set_ctv_filter(self, channel_type: enums.ChannelTypeVewFilter) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:CTVFilter \n
		Snippet: driver.configure.multiEval.set_ctv_filter(channel_type = enums.ChannelTypeVewFilter.OFF) \n
		Specifies, enables or disables the channel type view filter. If the filter is active, only slots with detected channel
		type PUSCH or PUCCH are measured. \n
			:param channel_type: PUSCh | PUCCh | ON | OFF PUSCh: measure only physical uplink shared channel PUCCh: measure only physical uplink control channel ON: enable the filter OFF: disable the filter
		"""
		param = Conversions.enum_scalar_to_str(channel_type, enums.ChannelTypeVewFilter)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:CTVFilter {param}')

	def get_dss_pusch(self) -> int:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:DSSPusch \n
		Snippet: value: int = driver.configure.multiEval.get_dss_pusch() \n
		Specifies the delta sequence shift value (Δss) used to calculate the sequence shift pattern for PUSCH. \n
			:return: delta_seq_sh_push: Range: 0 to 29
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:MEValuation:DSSPusch?')
		return Conversions.str_to_int(response)

	def set_dss_pusch(self, delta_seq_sh_push: int) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:DSSPusch \n
		Snippet: driver.configure.multiEval.set_dss_pusch(delta_seq_sh_push = 1) \n
		Specifies the delta sequence shift value (Δss) used to calculate the sequence shift pattern for PUSCH. \n
			:param delta_seq_sh_push: Range: 0 to 29
		"""
		param = Conversions.decimal_value_to_str(delta_seq_sh_push)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:DSSPusch {param}')

	def get_ghopping(self) -> bool:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:GHOPping \n
		Snippet: value: bool = driver.configure.multiEval.get_ghopping() \n
		Specifies whether group hopping is used or not. For the combined signal path scenario,
		useCONFigure:LTE:SIGN<i>:CONNection:GHOPping. \n
			:return: value: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:MEValuation:GHOPping?')
		return Conversions.str_to_bool(response)

	def set_ghopping(self, value: bool) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:GHOPping \n
		Snippet: driver.configure.multiEval.set_ghopping(value = False) \n
		Specifies whether group hopping is used or not. For the combined signal path scenario,
		useCONFigure:LTE:SIGN<i>:CONNection:GHOPping. \n
			:param value: OFF | ON
		"""
		param = Conversions.bool_to_str(value)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:GHOPping {param}')

	# noinspection PyTypeChecker
	class MsubFramesStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Subframe_Offset: int: Start of the measured subframe range relative to the trigger event Range: 0 to 9
			- Subframe_Count: int: Length of the measured subframe range Range: 1 to 320
			- Meas_Subframe: int: Subframe containing the measured slots for modulation and spectrum results Range: 0 to SubframeCount-1"""
		__meta_args_list = [
			ArgStruct.scalar_int('Subframe_Offset'),
			ArgStruct.scalar_int('Subframe_Count'),
			ArgStruct.scalar_int('Meas_Subframe')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Subframe_Offset: int = None
			self.Subframe_Count: int = None
			self.Meas_Subframe: int = None

	def get_msub_frames(self) -> MsubFramesStruct:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:MSUBframes \n
		Snippet: value: MsubFramesStruct = driver.configure.multiEval.get_msub_frames() \n
		Configures the scope of the measurement, i.e. which subframes are measured. \n
			:return: structure: for return value, see the help for MsubFramesStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:LTE:MEASurement<Instance>:MEValuation:MSUBframes?', self.__class__.MsubFramesStruct())

	def set_msub_frames(self, value: MsubFramesStruct) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:MSUBframes \n
		Snippet: driver.configure.multiEval.set_msub_frames(value = MsubFramesStruct()) \n
		Configures the scope of the measurement, i.e. which subframes are measured. \n
			:param value: see the help for MsubFramesStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:LTE:MEASurement<Instance>:MEValuation:MSUBframes', value)

	# noinspection PyTypeChecker
	def get_mslot(self) -> enums.MeasureSlot:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:MSLot \n
		Snippet: value: enums.MeasureSlot = driver.configure.multiEval.get_mslot() \n
		Selects which slots of the 'Measure Subframe' are measured. \n
			:return: measure_slot: MS0 | MS1 | ALL MS0: slot number 0 only MS1: slot number 1 only ALL: both slots
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:MEValuation:MSLot?')
		return Conversions.str_to_scalar_enum(response, enums.MeasureSlot)

	def set_mslot(self, measure_slot: enums.MeasureSlot) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:MSLot \n
		Snippet: driver.configure.multiEval.set_mslot(measure_slot = enums.MeasureSlot.ALL) \n
		Selects which slots of the 'Measure Subframe' are measured. \n
			:param measure_slot: MS0 | MS1 | ALL MS0: slot number 0 only MS1: slot number 1 only ALL: both slots
		"""
		param = Conversions.enum_scalar_to_str(measure_slot, enums.MeasureSlot)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:MSLot {param}')

	def clone(self) -> 'MultiEval':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MultiEval(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

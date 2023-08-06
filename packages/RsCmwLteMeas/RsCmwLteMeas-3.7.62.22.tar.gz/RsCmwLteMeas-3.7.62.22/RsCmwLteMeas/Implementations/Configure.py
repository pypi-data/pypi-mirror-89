from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal import Conversions
from .. import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Configure:
	"""Configure commands group definition. 199 total commands, 8 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("configure", core, parent)

	@property
	def rfSettings(self):
		"""rfSettings commands group. 2 Sub-classes, 5 commands."""
		if not hasattr(self, '_rfSettings'):
			from .Configure_.RfSettings import RfSettings
			self._rfSettings = RfSettings(self._core, self._base)
		return self._rfSettings

	@property
	def carrierAggregation(self):
		"""carrierAggregation commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_carrierAggregation'):
			from .Configure_.CarrierAggregation import CarrierAggregation
			self._carrierAggregation = CarrierAggregation(self._core, self._base)
		return self._carrierAggregation

	@property
	def emtc(self):
		"""emtc commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_emtc'):
			from .Configure_.Emtc import Emtc
			self._emtc = Emtc(self._core, self._base)
		return self._emtc

	@property
	def multiEval(self):
		"""multiEval commands group. 15 Sub-classes, 19 commands."""
		if not hasattr(self, '_multiEval'):
			from .Configure_.MultiEval import MultiEval
			self._multiEval = MultiEval(self._core, self._base)
		return self._multiEval

	@property
	def pcc(self):
		"""pcc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pcc'):
			from .Configure_.Pcc import Pcc
			self._pcc = Pcc(self._core, self._base)
		return self._pcc

	@property
	def cc(self):
		"""cc commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_cc'):
			from .Configure_.Cc import Cc
			self._cc = Cc(self._core, self._base)
		return self._cc

	@property
	def prach(self):
		"""prach commands group. 6 Sub-classes, 7 commands."""
		if not hasattr(self, '_prach'):
			from .Configure_.Prach import Prach
			self._prach = Prach(self._core, self._base)
		return self._prach

	@property
	def srs(self):
		"""srs commands group. 2 Sub-classes, 5 commands."""
		if not hasattr(self, '_srs'):
			from .Configure_.Srs import Srs
			self._srs = Srs(self._core, self._base)
		return self._srs

	# noinspection PyTypeChecker
	def get_band(self) -> enums.Band:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:BAND \n
		Snippet: value: enums.Band = driver.configure.get_band() \n
		Selects the operating band (OB) .
			INTRO_CMD_HELP: The allowed input range has dependencies: \n
			- FDD UL: OB1 | ... | OB28 | OB30 | OB31 | OB65 | OB66 | OB68 | OB70 | ... | OB74 | OB85
			- TDD UL: OB33 | ... | OB45 | OB48 | OB50 | ... | OB52 | OB250
			- Sidelink: OB47
			INTRO_CMD_HELP: For the combined signal path scenario, use: \n
			- CONFigure:LTE:BAND
			- CONFigure:LTE:SIGN<i>:SCC<c>:BAND \n
			:return: band: OB1 to OB250, see list above
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:BAND?')
		return Conversions.str_to_scalar_enum(response, enums.Band)

	def set_band(self, band: enums.Band) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:BAND \n
		Snippet: driver.configure.set_band(band = enums.Band.OB1) \n
		Selects the operating band (OB) .
			INTRO_CMD_HELP: The allowed input range has dependencies: \n
			- FDD UL: OB1 | ... | OB28 | OB30 | OB31 | OB65 | OB66 | OB68 | OB70 | ... | OB74 | OB85
			- TDD UL: OB33 | ... | OB45 | OB48 | OB50 | ... | OB52 | OB250
			- Sidelink: OB47
			INTRO_CMD_HELP: For the combined signal path scenario, use: \n
			- CONFigure:LTE:BAND
			- CONFigure:LTE:SIGN<i>:SCC<c>:BAND \n
			:param band: OB1 to OB250, see list above
		"""
		param = Conversions.enum_scalar_to_str(band, enums.Band)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:BAND {param}')

	# noinspection PyTypeChecker
	def get_stype(self) -> enums.SignalType:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:STYPe \n
		Snippet: value: enums.SignalType = driver.configure.get_stype() \n
		Selects the type of the measured signal. \n
			:return: signal_type: UL | SL UL: LTE uplink signal with PUSCH or PUCCH SL: V2X sidelink signal with PSSCH and PSCCH
		"""
		response = self._core.io.query_str_with_opc('CONFigure:LTE:MEASurement<Instance>:STYPe?')
		return Conversions.str_to_scalar_enum(response, enums.SignalType)

	def set_stype(self, signal_type: enums.SignalType) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:STYPe \n
		Snippet: driver.configure.set_stype(signal_type = enums.SignalType.SL) \n
		Selects the type of the measured signal. \n
			:param signal_type: UL | SL UL: LTE uplink signal with PUSCH or PUCCH SL: V2X sidelink signal with PSSCH and PSCCH
		"""
		param = Conversions.enum_scalar_to_str(signal_type, enums.SignalType)
		self._core.io.write_with_opc(f'CONFigure:LTE:MEASurement<Instance>:STYPe {param}')

	# noinspection PyTypeChecker
	def get_dmode(self) -> enums.DuplexMode:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:DMODe \n
		Snippet: value: enums.DuplexMode = driver.configure.get_dmode() \n
		Selects the duplex mode of the LTE signal: FDD or TDD.
			INTRO_CMD_HELP: For the combined signal path scenario, use: \n
			- CONFigure:LTE:DMODe
			- CONFigure:LTE:SIGN<i>:SCC<c>:DMODe
			- CONFigure:LTE:DMODe:UCSPecific \n
			:return: mode: FDD | TDD
		"""
		response = self._core.io.query_str_with_opc('CONFigure:LTE:MEASurement<Instance>:DMODe?')
		return Conversions.str_to_scalar_enum(response, enums.DuplexMode)

	def set_dmode(self, mode: enums.DuplexMode) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:DMODe \n
		Snippet: driver.configure.set_dmode(mode = enums.DuplexMode.FDD) \n
		Selects the duplex mode of the LTE signal: FDD or TDD.
			INTRO_CMD_HELP: For the combined signal path scenario, use: \n
			- CONFigure:LTE:DMODe
			- CONFigure:LTE:SIGN<i>:SCC<c>:DMODe
			- CONFigure:LTE:DMODe:UCSPecific \n
			:param mode: FDD | TDD
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.DuplexMode)
		self._core.io.write_with_opc(f'CONFigure:LTE:MEASurement<Instance>:DMODe {param}')

	# noinspection PyTypeChecker
	def get_fstructure(self) -> enums.FrameStructure:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:FSTRucture \n
		Snippet: value: enums.FrameStructure = driver.configure.get_fstructure() \n
		Queries the frame structure type of the LTE signal. The value depends on the duplex mode (method RsCmwLteMeas.Configure.
		dmode) . \n
			:return: frame_structure: T1 | T2 T1: Type 1, FDD signal T2: Type 2, TDD signal
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:FSTRucture?')
		return Conversions.str_to_scalar_enum(response, enums.FrameStructure)

	def clone(self) -> 'Configure':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Configure(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

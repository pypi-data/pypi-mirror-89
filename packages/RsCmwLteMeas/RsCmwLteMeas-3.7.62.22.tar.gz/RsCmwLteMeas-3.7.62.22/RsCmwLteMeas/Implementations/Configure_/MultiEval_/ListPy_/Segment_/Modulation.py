from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Modulation:
	"""Modulation commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("modulation", core, parent)

	# noinspection PyTypeChecker
	class ModulationStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Mod_Statistics: int: Statistical length in slots Range: 1 to 1000
			- Mod_Enable: bool: OFF | ON Enable or disable the measurement of modulation results ON: Modulation results are measured according to the other enable flags in this command. Modulation results for which there is no explicit enable flag are also measured (e.g. I/Q offset, frequency error and timing error) . OFF: No modulation results at all are measured. The other enable flags in this command are ignored.
			- Evmenable: bool: OFF | ON Enable or disable measurement of EVM
			- Mag_Error_Enable: bool: OFF | ON Enable or disable measurement of magnitude error
			- Phase_Err_Enable: bool: OFF | ON Enable or disable measurement of phase error
			- Ib_Eenable: bool: OFF | ON Enable or disable measurement of inband emissions
			- Eq_Sp_Flat_Enable: bool: OFF | ON Enable or disable measurement of equalizer spectrum flatness results
			- Mod_Scheme: enums.ModScheme: AUTO | QPSK | Q16 | Q64 | Q256 Modulation scheme used by the LTE uplink signal AUTO: automatic detection QPSK: QPSK Q16: 16-QAM Q64: 64-QAM Q256: 256-QAM"""
		__meta_args_list = [
			ArgStruct.scalar_int('Mod_Statistics'),
			ArgStruct.scalar_bool('Mod_Enable'),
			ArgStruct.scalar_bool('Evmenable'),
			ArgStruct.scalar_bool('Mag_Error_Enable'),
			ArgStruct.scalar_bool('Phase_Err_Enable'),
			ArgStruct.scalar_bool('Ib_Eenable'),
			ArgStruct.scalar_bool('Eq_Sp_Flat_Enable'),
			ArgStruct.scalar_enum('Mod_Scheme', enums.ModScheme)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Mod_Statistics: int = None
			self.Mod_Enable: bool = None
			self.Evmenable: bool = None
			self.Mag_Error_Enable: bool = None
			self.Phase_Err_Enable: bool = None
			self.Ib_Eenable: bool = None
			self.Eq_Sp_Flat_Enable: bool = None
			self.Mod_Scheme: enums.ModScheme = None

	def set(self, structure: ModulationStruct, segment=repcap.Segment.Default) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>:MODulation \n
		Snippet: driver.configure.multiEval.listPy.segment.modulation.set(value = [PROPERTY_STRUCT_NAME](), segment = repcap.Segment.Default) \n
		Defines settings for modulation measurements in list mode for segment <no>. \n
			:param structure: for set value, see the help for ModulationStruct structure arguments.
			:param segment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')"""
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		self._core.io.write_struct(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:MODulation', structure)

	def get(self, segment=repcap.Segment.Default) -> ModulationStruct:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>:MODulation \n
		Snippet: value: ModulationStruct = driver.configure.multiEval.listPy.segment.modulation.get(segment = repcap.Segment.Default) \n
		Defines settings for modulation measurements in list mode for segment <no>. \n
			:param segment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for ModulationStruct structure arguments."""
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		return self._core.io.query_struct(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:MODulation?', self.__class__.ModulationStruct())

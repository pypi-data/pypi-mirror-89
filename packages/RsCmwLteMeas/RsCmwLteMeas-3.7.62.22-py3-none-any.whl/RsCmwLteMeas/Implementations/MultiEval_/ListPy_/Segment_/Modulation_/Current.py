from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("current", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Seg_Reliability: int: Reliability indicator for the segment
			- Statist_Expired: int: Reached statistical length in slots
			- Out_Of_Tolerance: int: Percentage of measured subframes with failed limit check Unit: %
			- Evm_Rms_Low: float: EVM RMS value, low EVM window position Unit: %
			- Evm_Rms_High: float: EVM RMS value, high EVM window position Unit: %
			- Evmpeak_Low: float: EVM peak value, low EVM window position Unit: %
			- Evmpeak_High: float: EVM peak value, high EVM window position Unit: %
			- Mag_Error_Rms_Low: float: Magnitude error RMS value, low EVM window position Unit: %
			- Mag_Error_Rms_High: float: Magnitude error RMS value, low EVM window position Unit: %
			- Mag_Error_Peak_Low: float: Magnitude error peak value, low EVM window position Unit: %
			- Mag_Err_Peak_High: float: Magnitude error peak value, high EVM window position Unit: %
			- Ph_Error_Rms_Low: float: Phase error RMS value, low EVM window position Unit: deg
			- Ph_Error_Rms_High: float: Phase error RMS value, high EVM window position Unit: deg
			- Ph_Error_Peak_Low: float: Phase error peak value, low EVM window position Unit: deg
			- Ph_Error_Peak_High: float: Phase error peak value, high EVM window position Unit: deg
			- Iq_Offset: float: I/Q origin offset Unit: dBc
			- Frequency_Error: float: Carrier frequency error Unit: Hz
			- Timing_Error: float: Transmit time error Unit: Ts (basic LTE time unit)
			- Tx_Power: float: User equipment power Unit: dBm
			- Peak_Power: float: User equipment peak power Unit: dBm
			- Psd: float: No parameter help available
			- Evm_Dmrs_Low: float: EVM DMRS value, low EVM window position Unit: %
			- Evm_Dmrs_High: float: EVM DMRS value, high EVM window position Unit: %
			- Mag_Err_Dmrs_Low: float: Magnitude error DMRS value, low EVM window position Unit: %
			- Mag_Err_Dmrs_High: float: Magnitude error DMRS value, high EVM window position Unit: %
			- Ph_Error_Dmrs_Low: float: Phase error DMRS value, low EVM window position Unit: deg
			- Ph_Error_Dmrs_High: float: Phase error DMRS value, high EVM window position Unit: deg"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Seg_Reliability'),
			ArgStruct.scalar_int('Statist_Expired'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_float('Evm_Rms_Low'),
			ArgStruct.scalar_float('Evm_Rms_High'),
			ArgStruct.scalar_float('Evmpeak_Low'),
			ArgStruct.scalar_float('Evmpeak_High'),
			ArgStruct.scalar_float('Mag_Error_Rms_Low'),
			ArgStruct.scalar_float('Mag_Error_Rms_High'),
			ArgStruct.scalar_float('Mag_Error_Peak_Low'),
			ArgStruct.scalar_float('Mag_Err_Peak_High'),
			ArgStruct.scalar_float('Ph_Error_Rms_Low'),
			ArgStruct.scalar_float('Ph_Error_Rms_High'),
			ArgStruct.scalar_float('Ph_Error_Peak_Low'),
			ArgStruct.scalar_float('Ph_Error_Peak_High'),
			ArgStruct.scalar_float('Iq_Offset'),
			ArgStruct.scalar_float('Frequency_Error'),
			ArgStruct.scalar_float('Timing_Error'),
			ArgStruct.scalar_float('Tx_Power'),
			ArgStruct.scalar_float('Peak_Power'),
			ArgStruct.scalar_float('Psd'),
			ArgStruct.scalar_float('Evm_Dmrs_Low'),
			ArgStruct.scalar_float('Evm_Dmrs_High'),
			ArgStruct.scalar_float('Mag_Err_Dmrs_Low'),
			ArgStruct.scalar_float('Mag_Err_Dmrs_High'),
			ArgStruct.scalar_float('Ph_Error_Dmrs_Low'),
			ArgStruct.scalar_float('Ph_Error_Dmrs_High')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Seg_Reliability: int = None
			self.Statist_Expired: int = None
			self.Out_Of_Tolerance: int = None
			self.Evm_Rms_Low: float = None
			self.Evm_Rms_High: float = None
			self.Evmpeak_Low: float = None
			self.Evmpeak_High: float = None
			self.Mag_Error_Rms_Low: float = None
			self.Mag_Error_Rms_High: float = None
			self.Mag_Error_Peak_Low: float = None
			self.Mag_Err_Peak_High: float = None
			self.Ph_Error_Rms_Low: float = None
			self.Ph_Error_Rms_High: float = None
			self.Ph_Error_Peak_Low: float = None
			self.Ph_Error_Peak_High: float = None
			self.Iq_Offset: float = None
			self.Frequency_Error: float = None
			self.Timing_Error: float = None
			self.Tx_Power: float = None
			self.Peak_Power: float = None
			self.Psd: float = None
			self.Evm_Dmrs_Low: float = None
			self.Evm_Dmrs_High: float = None
			self.Mag_Err_Dmrs_Low: float = None
			self.Mag_Err_Dmrs_High: float = None
			self.Ph_Error_Dmrs_Low: float = None
			self.Ph_Error_Dmrs_High: float = None

	def fetch(self, segment=repcap.Segment.Default) -> FetchStruct:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>:MODulation:CURRent \n
		Snippet: value: FetchStruct = driver.multiEval.listPy.segment.modulation.current.fetch(segment = repcap.Segment.Default) \n
		Returns modulation single value results for segment <no> in list mode. The values described below are returned by FETCh
		commands. The first four values (reliability to out-of-tolerance result) are also returned by CALCulate commands.
		The remaining values returned by CALCulate commands are limit check results, one value for each result listed below. \n
			:param segment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		return self._core.io.query_struct(f'FETCh:LTE:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:MODulation:CURRent?', self.__class__.FetchStruct())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Seg_Reliability: int: Reliability indicator for the segment
			- Statist_Expired: int: Reached statistical length in slots
			- Out_Of_Tolerance: int: Percentage of measured subframes with failed limit check Unit: %
			- Evm_Rms_Low: float: EVM RMS value, low EVM window position Unit: %
			- Evm_Rms_High: float: EVM RMS value, high EVM window position Unit: %
			- Evmpeak_Low: float: EVM peak value, low EVM window position Unit: %
			- Evmpeak_High: float: EVM peak value, high EVM window position Unit: %
			- Mag_Error_Rms_Low: float: Magnitude error RMS value, low EVM window position Unit: %
			- Mag_Error_Rms_High: float: Magnitude error RMS value, low EVM window position Unit: %
			- Mag_Error_Peak_Low: float: Magnitude error peak value, low EVM window position Unit: %
			- Mag_Err_Peak_High: float: Magnitude error peak value, high EVM window position Unit: %
			- Ph_Error_Rms_Low: float: Phase error RMS value, low EVM window position Unit: deg
			- Ph_Error_Rms_High: float: Phase error RMS value, high EVM window position Unit: deg
			- Ph_Error_Peak_Low: float: Phase error peak value, low EVM window position Unit: deg
			- Ph_Error_Peak_High: float: Phase error peak value, high EVM window position Unit: deg
			- Iq_Offset: float: I/Q origin offset Unit: dBc
			- Frequency_Error: float: Carrier frequency error Unit: Hz
			- Timing_Error: float: Transmit time error Unit: Ts (basic LTE time unit)
			- Tx_Power: float: User equipment power Unit: dBm
			- Peak_Power: float: User equipment peak power Unit: dBm
			- Psd: float: No parameter help available
			- Evm_Dmrs_Low: float: EVM DMRS value, low EVM window position Unit: %
			- Evm_Dmrs_High: float: EVM DMRS value, high EVM window position Unit: %
			- Mag_Err_Dmrs_Low: float: Magnitude error DMRS value, low EVM window position Unit: %
			- Mag_Err_Dmrs_High: float: Magnitude error DMRS value, high EVM window position Unit: %
			- Ph_Error_Dmrs_Low: float: Phase error DMRS value, low EVM window position Unit: deg
			- Ph_Error_Dmrs_High: float: Phase error DMRS value, high EVM window position Unit: deg"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Seg_Reliability'),
			ArgStruct.scalar_int('Statist_Expired'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_float('Evm_Rms_Low'),
			ArgStruct.scalar_float('Evm_Rms_High'),
			ArgStruct.scalar_float('Evmpeak_Low'),
			ArgStruct.scalar_float('Evmpeak_High'),
			ArgStruct.scalar_float('Mag_Error_Rms_Low'),
			ArgStruct.scalar_float('Mag_Error_Rms_High'),
			ArgStruct.scalar_float('Mag_Error_Peak_Low'),
			ArgStruct.scalar_float('Mag_Err_Peak_High'),
			ArgStruct.scalar_float('Ph_Error_Rms_Low'),
			ArgStruct.scalar_float('Ph_Error_Rms_High'),
			ArgStruct.scalar_float('Ph_Error_Peak_Low'),
			ArgStruct.scalar_float('Ph_Error_Peak_High'),
			ArgStruct.scalar_float('Iq_Offset'),
			ArgStruct.scalar_float('Frequency_Error'),
			ArgStruct.scalar_float('Timing_Error'),
			ArgStruct.scalar_float('Tx_Power'),
			ArgStruct.scalar_float('Peak_Power'),
			ArgStruct.scalar_float('Psd'),
			ArgStruct.scalar_float('Evm_Dmrs_Low'),
			ArgStruct.scalar_float('Evm_Dmrs_High'),
			ArgStruct.scalar_float('Mag_Err_Dmrs_Low'),
			ArgStruct.scalar_float('Mag_Err_Dmrs_High'),
			ArgStruct.scalar_float('Ph_Error_Dmrs_Low'),
			ArgStruct.scalar_float('Ph_Error_Dmrs_High')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Seg_Reliability: int = None
			self.Statist_Expired: int = None
			self.Out_Of_Tolerance: int = None
			self.Evm_Rms_Low: float = None
			self.Evm_Rms_High: float = None
			self.Evmpeak_Low: float = None
			self.Evmpeak_High: float = None
			self.Mag_Error_Rms_Low: float = None
			self.Mag_Error_Rms_High: float = None
			self.Mag_Error_Peak_Low: float = None
			self.Mag_Err_Peak_High: float = None
			self.Ph_Error_Rms_Low: float = None
			self.Ph_Error_Rms_High: float = None
			self.Ph_Error_Peak_Low: float = None
			self.Ph_Error_Peak_High: float = None
			self.Iq_Offset: float = None
			self.Frequency_Error: float = None
			self.Timing_Error: float = None
			self.Tx_Power: float = None
			self.Peak_Power: float = None
			self.Psd: float = None
			self.Evm_Dmrs_Low: float = None
			self.Evm_Dmrs_High: float = None
			self.Mag_Err_Dmrs_Low: float = None
			self.Mag_Err_Dmrs_High: float = None
			self.Ph_Error_Dmrs_Low: float = None
			self.Ph_Error_Dmrs_High: float = None

	def calculate(self, segment=repcap.Segment.Default) -> CalculateStruct:
		"""SCPI: CALCulate:LTE:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>:MODulation:CURRent \n
		Snippet: value: CalculateStruct = driver.multiEval.listPy.segment.modulation.current.calculate(segment = repcap.Segment.Default) \n
		Returns modulation single value results for segment <no> in list mode. The values described below are returned by FETCh
		commands. The first four values (reliability to out-of-tolerance result) are also returned by CALCulate commands.
		The remaining values returned by CALCulate commands are limit check results, one value for each result listed below. \n
			:param segment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		return self._core.io.query_struct(f'CALCulate:LTE:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:MODulation:CURRent?', self.__class__.CalculateStruct())

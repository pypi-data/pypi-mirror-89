from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Maximum:
	"""Maximum commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("maximum", core, parent)

	def read(self, rBWkHz=repcap.RBWkHz.Default) -> List[float]:
		"""SCPI: READ:LTE:MEASurement<Instance>:MEValuation:TRACe:SEMask:RBW<kHz>:MAXimum \n
		Snippet: value: List[float] = driver.multiEval.trace.seMask.rbw.maximum.read(rBWkHz = repcap.RBWkHz.Default) \n
		Returns the values of the spectrum emission traces. Separate traces are available for the individual resolution
		bandwidths (<kHz>) . The results of the current, average and maximum traces can be retrieved. See also 'View Spectrum
		Emission Mask'. \n
		Use RsCmwLteMeas.reliability.last_value to read the updated reliability indicator. \n
			:param rBWkHz: optional repeated capability selector. Default value: Rbw30 (settable in the interface 'Rbw')
			:return: power: Comma-separated list of power results The value in the middle of the result array corresponds to the center frequency. The test point separation between two results depends on the resolution bandwidth, see table below. For RBW100 and greater, results are only available for frequencies with active limits using these RBWs. For other frequencies, INV is returned. Unit: dBm"""
		rBWkHz_cmd_val = self._base.get_repcap_cmd_value(rBWkHz, repcap.RBWkHz)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:LTE:MEASurement<Instance>:MEValuation:TRACe:SEMask:RBW{rBWkHz_cmd_val}:MAXimum?', suppressed)
		return response

	def fetch(self, rBWkHz=repcap.RBWkHz.Default) -> List[float]:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:TRACe:SEMask:RBW<kHz>:MAXimum \n
		Snippet: value: List[float] = driver.multiEval.trace.seMask.rbw.maximum.fetch(rBWkHz = repcap.RBWkHz.Default) \n
		Returns the values of the spectrum emission traces. Separate traces are available for the individual resolution
		bandwidths (<kHz>) . The results of the current, average and maximum traces can be retrieved. See also 'View Spectrum
		Emission Mask'. \n
		Use RsCmwLteMeas.reliability.last_value to read the updated reliability indicator. \n
			:param rBWkHz: optional repeated capability selector. Default value: Rbw30 (settable in the interface 'Rbw')
			:return: power: Comma-separated list of power results The value in the middle of the result array corresponds to the center frequency. The test point separation between two results depends on the resolution bandwidth, see table below. For RBW100 and greater, results are only available for frequencies with active limits using these RBWs. For other frequencies, INV is returned. Unit: dBm"""
		rBWkHz_cmd_val = self._base.get_repcap_cmd_value(rBWkHz, repcap.RBWkHz)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:LTE:MEASurement<Instance>:MEValuation:TRACe:SEMask:RBW{rBWkHz_cmd_val}:MAXimum?', suppressed)
		return response

from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .......Internal.Types import DataType
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Average:
	"""Average commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("average", core, parent)

	def fetch(self, utraAdjChannel=repcap.UtraAdjChannel.Default) -> List[float]:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:LIST:ACLR:UTRA<nr>:NEGativ:AVERage \n
		Snippet: value: List[float] = driver.multiEval.listPy.aclr.utra.negativ.average.fetch(utraAdjChannel = repcap.UtraAdjChannel.Default) \n
		Return the ACLR for the first or second adjacent UTRA channel above (POSitiv) or below (NEGativ) the carrier frequency
		for all measured list mode segments. The values described below are returned by FETCh commands. CALCulate commands return
		limit check results instead, one value for each result listed below. \n
		Use RsCmwLteMeas.reliability.last_value to read the updated reliability indicator. \n
			:param utraAdjChannel: optional repeated capability selector. Default value: Ch1 (settable in the interface 'Utra')
			:return: utra_negativ: No help available"""
		utraAdjChannel_cmd_val = self._base.get_repcap_cmd_value(utraAdjChannel, repcap.UtraAdjChannel)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:LTE:MEASurement<Instance>:MEValuation:LIST:ACLR:UTRA{utraAdjChannel_cmd_val}:NEGativ:AVERage?', suppressed)
		return response

	# noinspection PyTypeChecker
	def calculate(self, utraAdjChannel=repcap.UtraAdjChannel.Default) -> List[enums.ResultStatus2]:
		"""SCPI: CALCulate:LTE:MEASurement<Instance>:MEValuation:LIST:ACLR:UTRA<nr>:NEGativ:AVERage \n
		Snippet: value: List[enums.ResultStatus2] = driver.multiEval.listPy.aclr.utra.negativ.average.calculate(utraAdjChannel = repcap.UtraAdjChannel.Default) \n
		Return the ACLR for the first or second adjacent UTRA channel above (POSitiv) or below (NEGativ) the carrier frequency
		for all measured list mode segments. The values described below are returned by FETCh commands. CALCulate commands return
		limit check results instead, one value for each result listed below. \n
		Use RsCmwLteMeas.reliability.last_value to read the updated reliability indicator. \n
			:param utraAdjChannel: optional repeated capability selector. Default value: Ch1 (settable in the interface 'Utra')
			:return: utra_negativ: No help available"""
		utraAdjChannel_cmd_val = self._base.get_repcap_cmd_value(utraAdjChannel, repcap.UtraAdjChannel)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'CALCulate:LTE:MEASurement<Instance>:MEValuation:LIST:ACLR:UTRA{utraAdjChannel_cmd_val}:NEGativ:AVERage?', suppressed)
		return Conversions.str_to_list_enum(response, enums.ResultStatus2)

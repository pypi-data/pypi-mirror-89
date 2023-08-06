from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DchType:
	"""DchType commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dchType", core, parent)

	# noinspection PyTypeChecker
	def fetch(self) -> List[enums.UplinkChannelType]:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:LIST:MODulation:DCHType \n
		Snippet: value: List[enums.UplinkChannelType] = driver.multiEval.listPy.modulation.dchType.fetch() \n
		Return the uplink channel type for all measured list mode segments. The result is determined from the last measured slot
		of the statistical length of a segment. The individual measurements provide identical detected channel type results when
		measuring the same slot. However different statistical lengths can be defined for the measurements so that the measured
		slots and returned results can differ. \n
		Use RsCmwLteMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: channel_type: PUSCh | PUCCh Comma-separated list of values, one per measured segment"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:LTE:MEASurement<Instance>:MEValuation:LIST:MODulation:DCHType?', suppressed)
		return Conversions.str_to_list_enum(response, enums.UplinkChannelType)

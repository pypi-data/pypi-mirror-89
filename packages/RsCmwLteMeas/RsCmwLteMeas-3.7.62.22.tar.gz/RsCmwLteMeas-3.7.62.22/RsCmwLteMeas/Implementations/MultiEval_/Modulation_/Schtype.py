from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ....Internal.Types import DataType
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Schtype:
	"""Schtype commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("schtype", core, parent)

	# noinspection PyTypeChecker
	def fetch(self) -> enums.SidelinkChannelType:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:MODulation:SCHType \n
		Snippet: value: enums.SidelinkChannelType = driver.multiEval.modulation.schtype.fetch() \n
		Returns the sidelink channel type evaluated for modulation results. \n
		Use RsCmwLteMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: channel_type: PSSCh | PSCCh"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:LTE:MEASurement<Instance>:MEValuation:MODulation:SCHType?', suppressed)
		return Conversions.str_to_scalar_enum(response, enums.SidelinkChannelType)

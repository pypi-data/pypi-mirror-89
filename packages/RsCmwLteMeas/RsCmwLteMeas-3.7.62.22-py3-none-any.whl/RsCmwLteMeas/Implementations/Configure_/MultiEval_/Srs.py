from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Srs:
	"""Srs commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("srs", core, parent)

	def get_enable(self) -> bool:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:SRS:ENABle \n
		Snippet: value: bool = driver.configure.multiEval.srs.get_enable() \n
		Specifies whether a sounding reference signal is allowed (ON) or not (OFF) . For the combined signal path scenario, use
		CONFigure:LTE:SIGN<i>:SRS:ENABle. \n
			:return: enable: OFF | ON OFF: no SRS signal ON: SRS signal allowed in the last SC-FDMA symbol of each subframe
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:MEValuation:SRS:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, enable: bool) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:SRS:ENABle \n
		Snippet: driver.configure.multiEval.srs.set_enable(enable = False) \n
		Specifies whether a sounding reference signal is allowed (ON) or not (OFF) . For the combined signal path scenario, use
		CONFigure:LTE:SIGN<i>:SRS:ENABle. \n
			:param enable: OFF | ON OFF: no SRS signal ON: SRS signal allowed in the last SC-FDMA symbol of each subframe
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:SRS:ENABle {param}')

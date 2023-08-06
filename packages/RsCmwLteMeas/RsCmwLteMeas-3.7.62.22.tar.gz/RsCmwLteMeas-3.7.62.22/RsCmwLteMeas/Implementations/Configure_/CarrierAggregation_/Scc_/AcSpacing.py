from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AcSpacing:
	"""AcSpacing commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("acSpacing", core, parent)

	def set(self, secondaryCC=repcap.SecondaryCC.Default) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:CAGGregation[:SCC<Nr>]:ACSPacing \n
		Snippet: driver.configure.carrierAggregation.scc.acSpacing.set(secondaryCC = repcap.SecondaryCC.Default) \n
		Adjusts the component carrier frequencies, so that the carriers are aggregated contiguously. For the combined signal path
		scenario, useCONFigure:LTE:SIGN<i>:CAGGregation:SET. \n
			:param secondaryCC: optional repeated capability selector. Default value: CC1 (settable in the interface 'Scc')"""
		secondaryCC_cmd_val = self._base.get_repcap_cmd_value(secondaryCC, repcap.SecondaryCC)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:CAGGregation:SCC{secondaryCC_cmd_val}:ACSPacing')

	def set_with_opc(self, secondaryCC=repcap.SecondaryCC.Default) -> None:
		secondaryCC_cmd_val = self._base.get_repcap_cmd_value(secondaryCC, repcap.SecondaryCC)
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:CAGGregation[:SCC<Nr>]:ACSPacing \n
		Snippet: driver.configure.carrierAggregation.scc.acSpacing.set_with_opc(secondaryCC = repcap.SecondaryCC.Default) \n
		Adjusts the component carrier frequencies, so that the carriers are aggregated contiguously. For the combined signal path
		scenario, useCONFigure:LTE:SIGN<i>:CAGGregation:SET. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCmwLteMeas.utilities.opc_timeout_set() to set the timeout value. \n
			:param secondaryCC: optional repeated capability selector. Default value: CC1 (settable in the interface 'Scc')"""
		self._core.io.write_with_opc(f'CONFigure:LTE:MEASurement<Instance>:CAGGregation:SCC{secondaryCC_cmd_val}:ACSPacing')

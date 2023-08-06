from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Enhanced:
	"""Enhanced commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("enhanced", core, parent)

	def set(self, meas_carrier: enums.MeasCarrierEnhanced, segment=repcap.Segment.Default) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>:CAGGregation:MCARrier:ENHanced \n
		Snippet: driver.configure.multiEval.listPy.segment.carrierAggregation.mcarrier.enhanced.set(meas_carrier = enums.MeasCarrierEnhanced.CC1, segment = repcap.Segment.Default) \n
		Selects a component carrier for single-carrier measurements in segment <no>. \n
			:param meas_carrier: CC1 | CC2 | CC3 | CC4
			:param segment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')"""
		param = Conversions.enum_scalar_to_str(meas_carrier, enums.MeasCarrierEnhanced)
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:CAGGregation:MCARrier:ENHanced {param}')

	# noinspection PyTypeChecker
	def get(self, segment=repcap.Segment.Default) -> enums.MeasCarrierEnhanced:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>:CAGGregation:MCARrier:ENHanced \n
		Snippet: value: enums.MeasCarrierEnhanced = driver.configure.multiEval.listPy.segment.carrierAggregation.mcarrier.enhanced.get(segment = repcap.Segment.Default) \n
		Selects a component carrier for single-carrier measurements in segment <no>. \n
			:param segment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: meas_carrier: CC1 | CC2 | CC3 | CC4"""
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		response = self._core.io.query_str(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:CAGGregation:MCARrier:ENHanced?')
		return Conversions.str_to_scalar_enum(response, enums.MeasCarrierEnhanced)

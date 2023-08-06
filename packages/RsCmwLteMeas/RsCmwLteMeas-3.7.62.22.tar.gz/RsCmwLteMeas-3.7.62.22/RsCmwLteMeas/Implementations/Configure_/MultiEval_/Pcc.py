from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pcc:
	"""Pcc commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pcc", core, parent)

	def get_plc_id(self) -> int:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation[:PCC]:PLCid \n
		Snippet: value: int = driver.configure.multiEval.pcc.get_plc_id() \n
		No command help available \n
			:return: phs_layer_cell_id: No help available
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:MEValuation:PCC:PLCid?')
		return Conversions.str_to_int(response)

	def set_plc_id(self, phs_layer_cell_id: int) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation[:PCC]:PLCid \n
		Snippet: driver.configure.multiEval.pcc.set_plc_id(phs_layer_cell_id = 1) \n
		No command help available \n
			:param phs_layer_cell_id: No help available
		"""
		param = Conversions.decimal_value_to_str(phs_layer_cell_id)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:PCC:PLCid {param}')

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pformat:
	"""Pformat commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: PreambleFormat, default value after init: PreambleFormat.Fmt1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pformat", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_preambleFormat_get', 'repcap_preambleFormat_set', repcap.PreambleFormat.Fmt1)

	def repcap_preambleFormat_set(self, enum_value: repcap.PreambleFormat) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to PreambleFormat.Default
		Default value after init: PreambleFormat.Fmt1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_preambleFormat_get(self) -> repcap.PreambleFormat:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def set(self, evmwindow_length: int, preambleFormat=repcap.PreambleFormat.Default) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:PRACh:MODulation:EWLength:PFORmat<PreambleFormat> \n
		Snippet: driver.configure.prach.modulation.ewLength.pformat.set(evmwindow_length = 1, preambleFormat = repcap.PreambleFormat.Default) \n
		No command help available \n
			:param evmwindow_length: No help available
			:param preambleFormat: optional repeated capability selector. Default value: Fmt1 (settable in the interface 'Pformat')"""
		param = Conversions.decimal_value_to_str(evmwindow_length)
		preambleFormat_cmd_val = self._base.get_repcap_cmd_value(preambleFormat, repcap.PreambleFormat)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:PRACh:MODulation:EWLength:PFORmat{preambleFormat_cmd_val} {param}')

	def get(self, preambleFormat=repcap.PreambleFormat.Default) -> int:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:PRACh:MODulation:EWLength:PFORmat<PreambleFormat> \n
		Snippet: value: int = driver.configure.prach.modulation.ewLength.pformat.get(preambleFormat = repcap.PreambleFormat.Default) \n
		No command help available \n
			:param preambleFormat: optional repeated capability selector. Default value: Fmt1 (settable in the interface 'Pformat')
			:return: evmwindow_length: No help available"""
		preambleFormat_cmd_val = self._base.get_repcap_cmd_value(preambleFormat, repcap.PreambleFormat)
		response = self._core.io.query_str(f'CONFigure:LTE:MEASurement<Instance>:PRACh:MODulation:EWLength:PFORmat{preambleFormat_cmd_val}?')
		return Conversions.str_to_int(response)

	def clone(self) -> 'Pformat':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Pformat(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Result:
	"""Result commands group definition. 9 total commands, 0 Sub-groups, 9 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("result", core, parent)

	# noinspection PyTypeChecker
	class AllStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Evm: bool: OFF | ON Error vector magnitude OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
			- Magnitude_Error: bool: OFF | ON Magnitude error
			- Phase_Error: bool: OFF | ON Phase error
			- Iq: bool: OFF | ON I/Q constellation diagram
			- Power_Dynamics: bool: OFF | ON Power dynamics
			- Tx_Measurement: bool: OFF | ON Statistical overview
			- Evmvs_Preamble: bool: OFF | ON Error vector magnitude vs preamble
			- Powervs_Preamble: bool: OFF | ON Power vs preamble"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Evm'),
			ArgStruct.scalar_bool('Magnitude_Error'),
			ArgStruct.scalar_bool('Phase_Error'),
			ArgStruct.scalar_bool('Iq'),
			ArgStruct.scalar_bool('Power_Dynamics'),
			ArgStruct.scalar_bool('Tx_Measurement'),
			ArgStruct.scalar_bool('Evmvs_Preamble'),
			ArgStruct.scalar_bool('Powervs_Preamble')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Evm: bool = None
			self.Magnitude_Error: bool = None
			self.Phase_Error: bool = None
			self.Iq: bool = None
			self.Power_Dynamics: bool = None
			self.Tx_Measurement: bool = None
			self.Evmvs_Preamble: bool = None
			self.Powervs_Preamble: bool = None

	def get_all(self) -> AllStruct:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:PRACh:RESult[:ALL] \n
		Snippet: value: AllStruct = driver.configure.prach.result.get_all() \n
		Enables or disables the evaluation of results and shows or hides the views in the PRACH measurement.
		This command combines all other CONFigure:LTE:MEAS<i>:PRACh:RESult... commands. \n
			:return: structure: for return value, see the help for AllStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:LTE:MEASurement<Instance>:PRACh:RESult:ALL?', self.__class__.AllStruct())

	def set_all(self, value: AllStruct) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:PRACh:RESult[:ALL] \n
		Snippet: driver.configure.prach.result.set_all(value = AllStruct()) \n
		Enables or disables the evaluation of results and shows or hides the views in the PRACH measurement.
		This command combines all other CONFigure:LTE:MEAS<i>:PRACh:RESult... commands. \n
			:param value: see the help for AllStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:LTE:MEASurement<Instance>:PRACh:RESult:ALL', value)

	def get_ev_magnitude(self) -> bool:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:PRACh:RESult:EVMagnitude \n
		Snippet: value: bool = driver.configure.prach.result.get_ev_magnitude() \n
		Enables or disables the evaluation of results and shows or hides the views in the PRACH measurement. The mnemonic after
		'RESult' denotes the view type: error vector magnitude, magnitude error, phase error, I/Q constellation diagram, power
		dynamics, TX measurement statistical overview, error vector magnitude vs preamble, power vs preamble For reset values,
		see CONFigure:LTE:MEAS<i>:PRACh. \n
			:return: enable: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:PRACh:RESult:EVMagnitude?')
		return Conversions.str_to_bool(response)

	def set_ev_magnitude(self, enable: bool) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:PRACh:RESult:EVMagnitude \n
		Snippet: driver.configure.prach.result.set_ev_magnitude(enable = False) \n
		Enables or disables the evaluation of results and shows or hides the views in the PRACH measurement. The mnemonic after
		'RESult' denotes the view type: error vector magnitude, magnitude error, phase error, I/Q constellation diagram, power
		dynamics, TX measurement statistical overview, error vector magnitude vs preamble, power vs preamble For reset values,
		see CONFigure:LTE:MEAS<i>:PRACh. \n
			:param enable: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:PRACh:RESult:EVMagnitude {param}')

	def get_ev_preamble(self) -> bool:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:PRACh:RESult:EVPReamble \n
		Snippet: value: bool = driver.configure.prach.result.get_ev_preamble() \n
		Enables or disables the evaluation of results and shows or hides the views in the PRACH measurement. The mnemonic after
		'RESult' denotes the view type: error vector magnitude, magnitude error, phase error, I/Q constellation diagram, power
		dynamics, TX measurement statistical overview, error vector magnitude vs preamble, power vs preamble For reset values,
		see CONFigure:LTE:MEAS<i>:PRACh. \n
			:return: enable: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:PRACh:RESult:EVPReamble?')
		return Conversions.str_to_bool(response)

	def set_ev_preamble(self, enable: bool) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:PRACh:RESult:EVPReamble \n
		Snippet: driver.configure.prach.result.set_ev_preamble(enable = False) \n
		Enables or disables the evaluation of results and shows or hides the views in the PRACH measurement. The mnemonic after
		'RESult' denotes the view type: error vector magnitude, magnitude error, phase error, I/Q constellation diagram, power
		dynamics, TX measurement statistical overview, error vector magnitude vs preamble, power vs preamble For reset values,
		see CONFigure:LTE:MEAS<i>:PRACh. \n
			:param enable: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:PRACh:RESult:EVPReamble {param}')

	def get_merror(self) -> bool:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:PRACh:RESult:MERRor \n
		Snippet: value: bool = driver.configure.prach.result.get_merror() \n
		Enables or disables the evaluation of results and shows or hides the views in the PRACH measurement. The mnemonic after
		'RESult' denotes the view type: error vector magnitude, magnitude error, phase error, I/Q constellation diagram, power
		dynamics, TX measurement statistical overview, error vector magnitude vs preamble, power vs preamble For reset values,
		see CONFigure:LTE:MEAS<i>:PRACh. \n
			:return: enable: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:PRACh:RESult:MERRor?')
		return Conversions.str_to_bool(response)

	def set_merror(self, enable: bool) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:PRACh:RESult:MERRor \n
		Snippet: driver.configure.prach.result.set_merror(enable = False) \n
		Enables or disables the evaluation of results and shows or hides the views in the PRACH measurement. The mnemonic after
		'RESult' denotes the view type: error vector magnitude, magnitude error, phase error, I/Q constellation diagram, power
		dynamics, TX measurement statistical overview, error vector magnitude vs preamble, power vs preamble For reset values,
		see CONFigure:LTE:MEAS<i>:PRACh. \n
			:param enable: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:PRACh:RESult:MERRor {param}')

	def get_perror(self) -> bool:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:PRACh:RESult:PERRor \n
		Snippet: value: bool = driver.configure.prach.result.get_perror() \n
		Enables or disables the evaluation of results and shows or hides the views in the PRACH measurement. The mnemonic after
		'RESult' denotes the view type: error vector magnitude, magnitude error, phase error, I/Q constellation diagram, power
		dynamics, TX measurement statistical overview, error vector magnitude vs preamble, power vs preamble For reset values,
		see CONFigure:LTE:MEAS<i>:PRACh. \n
			:return: enable: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:PRACh:RESult:PERRor?')
		return Conversions.str_to_bool(response)

	def set_perror(self, enable: bool) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:PRACh:RESult:PERRor \n
		Snippet: driver.configure.prach.result.set_perror(enable = False) \n
		Enables or disables the evaluation of results and shows or hides the views in the PRACH measurement. The mnemonic after
		'RESult' denotes the view type: error vector magnitude, magnitude error, phase error, I/Q constellation diagram, power
		dynamics, TX measurement statistical overview, error vector magnitude vs preamble, power vs preamble For reset values,
		see CONFigure:LTE:MEAS<i>:PRACh. \n
			:param enable: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:PRACh:RESult:PERRor {param}')

	def get_iq(self) -> bool:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:PRACh:RESult:IQ \n
		Snippet: value: bool = driver.configure.prach.result.get_iq() \n
		Enables or disables the evaluation of results and shows or hides the views in the PRACH measurement. The mnemonic after
		'RESult' denotes the view type: error vector magnitude, magnitude error, phase error, I/Q constellation diagram, power
		dynamics, TX measurement statistical overview, error vector magnitude vs preamble, power vs preamble For reset values,
		see CONFigure:LTE:MEAS<i>:PRACh. \n
			:return: enable: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:PRACh:RESult:IQ?')
		return Conversions.str_to_bool(response)

	def set_iq(self, enable: bool) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:PRACh:RESult:IQ \n
		Snippet: driver.configure.prach.result.set_iq(enable = False) \n
		Enables or disables the evaluation of results and shows or hides the views in the PRACH measurement. The mnemonic after
		'RESult' denotes the view type: error vector magnitude, magnitude error, phase error, I/Q constellation diagram, power
		dynamics, TX measurement statistical overview, error vector magnitude vs preamble, power vs preamble For reset values,
		see CONFigure:LTE:MEAS<i>:PRACh. \n
			:param enable: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:PRACh:RESult:IQ {param}')

	def get_pdynamics(self) -> bool:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:PRACh:RESult:PDYNamics \n
		Snippet: value: bool = driver.configure.prach.result.get_pdynamics() \n
		Enables or disables the evaluation of results and shows or hides the views in the PRACH measurement. The mnemonic after
		'RESult' denotes the view type: error vector magnitude, magnitude error, phase error, I/Q constellation diagram, power
		dynamics, TX measurement statistical overview, error vector magnitude vs preamble, power vs preamble For reset values,
		see CONFigure:LTE:MEAS<i>:PRACh. \n
			:return: enable: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:PRACh:RESult:PDYNamics?')
		return Conversions.str_to_bool(response)

	def set_pdynamics(self, enable: bool) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:PRACh:RESult:PDYNamics \n
		Snippet: driver.configure.prach.result.set_pdynamics(enable = False) \n
		Enables or disables the evaluation of results and shows or hides the views in the PRACH measurement. The mnemonic after
		'RESult' denotes the view type: error vector magnitude, magnitude error, phase error, I/Q constellation diagram, power
		dynamics, TX measurement statistical overview, error vector magnitude vs preamble, power vs preamble For reset values,
		see CONFigure:LTE:MEAS<i>:PRACh. \n
			:param enable: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:PRACh:RESult:PDYNamics {param}')

	def get_pv_preamble(self) -> bool:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:PRACh:RESult:PVPReamble \n
		Snippet: value: bool = driver.configure.prach.result.get_pv_preamble() \n
		Enables or disables the evaluation of results and shows or hides the views in the PRACH measurement. The mnemonic after
		'RESult' denotes the view type: error vector magnitude, magnitude error, phase error, I/Q constellation diagram, power
		dynamics, TX measurement statistical overview, error vector magnitude vs preamble, power vs preamble For reset values,
		see CONFigure:LTE:MEAS<i>:PRACh. \n
			:return: enable: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:PRACh:RESult:PVPReamble?')
		return Conversions.str_to_bool(response)

	def set_pv_preamble(self, enable: bool) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:PRACh:RESult:PVPReamble \n
		Snippet: driver.configure.prach.result.set_pv_preamble(enable = False) \n
		Enables or disables the evaluation of results and shows or hides the views in the PRACH measurement. The mnemonic after
		'RESult' denotes the view type: error vector magnitude, magnitude error, phase error, I/Q constellation diagram, power
		dynamics, TX measurement statistical overview, error vector magnitude vs preamble, power vs preamble For reset values,
		see CONFigure:LTE:MEAS<i>:PRACh. \n
			:param enable: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:PRACh:RESult:PVPReamble {param}')

	def get_txm(self) -> bool:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:PRACh:RESult:TXM \n
		Snippet: value: bool = driver.configure.prach.result.get_txm() \n
		Enables or disables the evaluation of results and shows or hides the views in the PRACH measurement. The mnemonic after
		'RESult' denotes the view type: error vector magnitude, magnitude error, phase error, I/Q constellation diagram, power
		dynamics, TX measurement statistical overview, error vector magnitude vs preamble, power vs preamble For reset values,
		see CONFigure:LTE:MEAS<i>:PRACh. \n
			:return: enable: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:PRACh:RESult:TXM?')
		return Conversions.str_to_bool(response)

	def set_txm(self, enable: bool) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:PRACh:RESult:TXM \n
		Snippet: driver.configure.prach.result.set_txm(enable = False) \n
		Enables or disables the evaluation of results and shows or hides the views in the PRACH measurement. The mnemonic after
		'RESult' denotes the view type: error vector magnitude, magnitude error, phase error, I/Q constellation diagram, power
		dynamics, TX measurement statistical overview, error vector magnitude vs preamble, power vs preamble For reset values,
		see CONFigure:LTE:MEAS<i>:PRACh. \n
			:param enable: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:PRACh:RESult:TXM {param}')

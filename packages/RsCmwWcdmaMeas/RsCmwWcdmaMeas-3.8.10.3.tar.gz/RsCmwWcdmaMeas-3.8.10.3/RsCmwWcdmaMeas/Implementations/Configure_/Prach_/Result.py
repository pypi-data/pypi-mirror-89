from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Result:
	"""Result commands group definition. 12 total commands, 1 Sub-groups, 8 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("result", core, parent)

	@property
	def chip(self):
		"""chip commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_chip'):
			from .Result_.Chip import Chip
			self._chip = Chip(self._core, self._base)
		return self._chip

	def get_ue_power(self) -> bool:
		"""SCPI: CONFigure:WCDMa:MEASurement<instance>:PRACh:RESult:UEPower \n
		Snippet: value: bool = driver.configure.prach.result.get_ue_power() \n
		Enables or disables the evaluation of results and shows or hides the UE power view in the PRACH measurement. \n
			:return: enable_ue_power: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		response = self._core.io.query_str('CONFigure:WCDMa:MEASurement<Instance>:PRACh:RESult:UEPower?')
		return Conversions.str_to_bool(response)

	def set_ue_power(self, enable_ue_power: bool) -> None:
		"""SCPI: CONFigure:WCDMa:MEASurement<instance>:PRACh:RESult:UEPower \n
		Snippet: driver.configure.prach.result.set_ue_power(enable_ue_power = False) \n
		Enables or disables the evaluation of results and shows or hides the UE power view in the PRACH measurement. \n
			:param enable_ue_power: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		param = Conversions.bool_to_str(enable_ue_power)
		self._core.io.write(f'CONFigure:WCDMa:MEASurement<Instance>:PRACh:RESult:UEPower {param}')

	def get_psteps(self) -> bool:
		"""SCPI: CONFigure:WCDMa:MEASurement<instance>:PRACh:RESult:PSTeps \n
		Snippet: value: bool = driver.configure.prach.result.get_psteps() \n
		Enables or disables the evaluation of results and shows or hides the power steps view in the PRACH measurement. \n
			:return: enable_pow_steps: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		response = self._core.io.query_str('CONFigure:WCDMa:MEASurement<Instance>:PRACh:RESult:PSTeps?')
		return Conversions.str_to_bool(response)

	def set_psteps(self, enable_pow_steps: bool) -> None:
		"""SCPI: CONFigure:WCDMa:MEASurement<instance>:PRACh:RESult:PSTeps \n
		Snippet: driver.configure.prach.result.set_psteps(enable_pow_steps = False) \n
		Enables or disables the evaluation of results and shows or hides the power steps view in the PRACH measurement. \n
			:param enable_pow_steps: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		param = Conversions.bool_to_str(enable_pow_steps)
		self._core.io.write(f'CONFigure:WCDMa:MEASurement<Instance>:PRACh:RESult:PSTeps {param}')

	def get_freq_error(self) -> bool:
		"""SCPI: CONFigure:WCDMa:MEASurement<instance>:PRACh:RESult:FERRor \n
		Snippet: value: bool = driver.configure.prach.result.get_freq_error() \n
		Enables or disables the evaluation of results and shows or hides the frequency error view in the PRACH measurement. \n
			:return: enable_freq_error: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		response = self._core.io.query_str('CONFigure:WCDMa:MEASurement<Instance>:PRACh:RESult:FERRor?')
		return Conversions.str_to_bool(response)

	def set_freq_error(self, enable_freq_error: bool) -> None:
		"""SCPI: CONFigure:WCDMa:MEASurement<instance>:PRACh:RESult:FERRor \n
		Snippet: driver.configure.prach.result.set_freq_error(enable_freq_error = False) \n
		Enables or disables the evaluation of results and shows or hides the frequency error view in the PRACH measurement. \n
			:param enable_freq_error: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		param = Conversions.bool_to_str(enable_freq_error)
		self._core.io.write(f'CONFigure:WCDMa:MEASurement<Instance>:PRACh:RESult:FERRor {param}')

	# noinspection PyTypeChecker
	class AllStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable_Ue_Power: bool: OFF | ON UE power OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
			- Enable_Pow_Steps: bool: OFF | ON Power steps
			- Enable_Freq_Error: bool: OFF | ON Frequency error
			- Enable_Evm: bool: OFF | ON Error vector magnitude
			- Enable_Mag_Error: bool: OFF | ON Magnitude error
			- Enable_Phase_Err: bool: OFF | ON Phase error
			- Enable_Ue_Pchip: bool: OFF | ON UE power vs. chip
			- Enable_Evmchip: bool: OFF | ON EVM vs. chip
			- Enable_Merr_Chip: bool: OFF | ON Magnitude error vs. chip
			- Enable_Ph_Err_Chip: bool: OFF | ON Phase error vs. chip
			- Enable_Iq: bool: OFF | ON I/Q constellation diagram"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable_Ue_Power'),
			ArgStruct.scalar_bool('Enable_Pow_Steps'),
			ArgStruct.scalar_bool('Enable_Freq_Error'),
			ArgStruct.scalar_bool('Enable_Evm'),
			ArgStruct.scalar_bool('Enable_Mag_Error'),
			ArgStruct.scalar_bool('Enable_Phase_Err'),
			ArgStruct.scalar_bool('Enable_Ue_Pchip'),
			ArgStruct.scalar_bool('Enable_Evmchip'),
			ArgStruct.scalar_bool('Enable_Merr_Chip'),
			ArgStruct.scalar_bool('Enable_Ph_Err_Chip'),
			ArgStruct.scalar_bool('Enable_Iq')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable_Ue_Power: bool = None
			self.Enable_Pow_Steps: bool = None
			self.Enable_Freq_Error: bool = None
			self.Enable_Evm: bool = None
			self.Enable_Mag_Error: bool = None
			self.Enable_Phase_Err: bool = None
			self.Enable_Ue_Pchip: bool = None
			self.Enable_Evmchip: bool = None
			self.Enable_Merr_Chip: bool = None
			self.Enable_Ph_Err_Chip: bool = None
			self.Enable_Iq: bool = None

	def get_all(self) -> AllStruct:
		"""SCPI: CONFigure:WCDMa:MEASurement<instance>:PRACh:RESult[:ALL] \n
		Snippet: value: AllStruct = driver.configure.prach.result.get_all() \n
		Enables or disables the evaluation of results and shows or hides the views in the PRACH measurement.
		This command combines all other CONFigure:WCDMa:MEAS<i>:PRACh:RESult... commands. \n
			:return: structure: for return value, see the help for AllStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WCDMa:MEASurement<Instance>:PRACh:RESult:ALL?', self.__class__.AllStruct())

	def set_all(self, value: AllStruct) -> None:
		"""SCPI: CONFigure:WCDMa:MEASurement<instance>:PRACh:RESult[:ALL] \n
		Snippet: driver.configure.prach.result.set_all(value = AllStruct()) \n
		Enables or disables the evaluation of results and shows or hides the views in the PRACH measurement.
		This command combines all other CONFigure:WCDMa:MEAS<i>:PRACh:RESult... commands. \n
			:param value: see the help for AllStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WCDMa:MEASurement<Instance>:PRACh:RESult:ALL', value)

	def get_perror(self) -> bool:
		"""SCPI: CONFigure:WCDMa:MEASurement<instance>:PRACh:RESult:PERRor \n
		Snippet: value: bool = driver.configure.prach.result.get_perror() \n
		Enables or disables the evaluation of results and shows or hides the phase error view in the PRACH measurement. \n
			:return: enable_phase_err: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		response = self._core.io.query_str('CONFigure:WCDMa:MEASurement<Instance>:PRACh:RESult:PERRor?')
		return Conversions.str_to_bool(response)

	def set_perror(self, enable_phase_err: bool) -> None:
		"""SCPI: CONFigure:WCDMa:MEASurement<instance>:PRACh:RESult:PERRor \n
		Snippet: driver.configure.prach.result.set_perror(enable_phase_err = False) \n
		Enables or disables the evaluation of results and shows or hides the phase error view in the PRACH measurement. \n
			:param enable_phase_err: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		param = Conversions.bool_to_str(enable_phase_err)
		self._core.io.write(f'CONFigure:WCDMa:MEASurement<Instance>:PRACh:RESult:PERRor {param}')

	def get_ev_magnitude(self) -> bool:
		"""SCPI: CONFigure:WCDMa:MEASurement<instance>:PRACh:RESult:EVMagnitude \n
		Snippet: value: bool = driver.configure.prach.result.get_ev_magnitude() \n
		Enables or disables the evaluation of results and shows or hides the error vector magnitude view in the PRACH measurement. \n
			:return: enable_evm: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		response = self._core.io.query_str('CONFigure:WCDMa:MEASurement<Instance>:PRACh:RESult:EVMagnitude?')
		return Conversions.str_to_bool(response)

	def set_ev_magnitude(self, enable_evm: bool) -> None:
		"""SCPI: CONFigure:WCDMa:MEASurement<instance>:PRACh:RESult:EVMagnitude \n
		Snippet: driver.configure.prach.result.set_ev_magnitude(enable_evm = False) \n
		Enables or disables the evaluation of results and shows or hides the error vector magnitude view in the PRACH measurement. \n
			:param enable_evm: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		param = Conversions.bool_to_str(enable_evm)
		self._core.io.write(f'CONFigure:WCDMa:MEASurement<Instance>:PRACh:RESult:EVMagnitude {param}')

	def get_merror(self) -> bool:
		"""SCPI: CONFigure:WCDMa:MEASurement<instance>:PRACh:RESult:MERRor \n
		Snippet: value: bool = driver.configure.prach.result.get_merror() \n
		Enables or disables the evaluation of results and shows or hides the magnitude error view in the PRACH measurement. \n
			:return: enable_mag_error: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		response = self._core.io.query_str('CONFigure:WCDMa:MEASurement<Instance>:PRACh:RESult:MERRor?')
		return Conversions.str_to_bool(response)

	def set_merror(self, enable_mag_error: bool) -> None:
		"""SCPI: CONFigure:WCDMa:MEASurement<instance>:PRACh:RESult:MERRor \n
		Snippet: driver.configure.prach.result.set_merror(enable_mag_error = False) \n
		Enables or disables the evaluation of results and shows or hides the magnitude error view in the PRACH measurement. \n
			:param enable_mag_error: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		param = Conversions.bool_to_str(enable_mag_error)
		self._core.io.write(f'CONFigure:WCDMa:MEASurement<Instance>:PRACh:RESult:MERRor {param}')

	def get_iq(self) -> bool:
		"""SCPI: CONFigure:WCDMa:MEASurement<instance>:PRACh:RESult:IQ \n
		Snippet: value: bool = driver.configure.prach.result.get_iq() \n
		Enables or disables the evaluation of results and shows or hides the I/Q constellation diagram view in the PRACH
		measurement. \n
			:return: enable_iq: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		response = self._core.io.query_str('CONFigure:WCDMa:MEASurement<Instance>:PRACh:RESult:IQ?')
		return Conversions.str_to_bool(response)

	def set_iq(self, enable_iq: bool) -> None:
		"""SCPI: CONFigure:WCDMa:MEASurement<instance>:PRACh:RESult:IQ \n
		Snippet: driver.configure.prach.result.set_iq(enable_iq = False) \n
		Enables or disables the evaluation of results and shows or hides the I/Q constellation diagram view in the PRACH
		measurement. \n
			:param enable_iq: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		param = Conversions.bool_to_str(enable_iq)
		self._core.io.write(f'CONFigure:WCDMa:MEASurement<Instance>:PRACh:RESult:IQ {param}')

	def clone(self) -> 'Result':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Result(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

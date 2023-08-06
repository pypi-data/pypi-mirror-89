from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Result:
	"""Result commands group definition. 15 total commands, 1 Sub-groups, 13 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("result", core, parent)

	@property
	def evMagnitude(self):
		"""evMagnitude commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_evMagnitude'):
			from .Result_.EvMagnitude import EvMagnitude
			self._evMagnitude = EvMagnitude(self._core, self._base)
		return self._evMagnitude

	def get_modulation(self) -> bool:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:MODulation \n
		Snippet: value: bool = driver.configure.nrMmwMeas.multiEval.result.get_modulation() \n
		Enables or disables the evaluation of results in the multi-evaluation measurement. \n
			:return: enable: OFF: Do not evaluate results ON: Evaluate results
		"""
		response = self._core.io.query_str('CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:MODulation?')
		return Conversions.str_to_bool(response)

	def set_modulation(self, enable: bool) -> None:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:MODulation \n
		Snippet: driver.configure.nrMmwMeas.multiEval.result.set_modulation(enable = False) \n
		Enables or disables the evaluation of results in the multi-evaluation measurement. \n
			:param enable: OFF: Do not evaluate results ON: Evaluate results
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:MODulation {param}')

	def get_se_mask(self) -> bool:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:SEMask \n
		Snippet: value: bool = driver.configure.nrMmwMeas.multiEval.result.get_se_mask() \n
		Enables or disables the evaluation of results in the multi-evaluation measurement. \n
			:return: enable: OFF: Do not evaluate results ON: Evaluate results
		"""
		response = self._core.io.query_str('CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:SEMask?')
		return Conversions.str_to_bool(response)

	def set_se_mask(self, enable: bool) -> None:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:SEMask \n
		Snippet: driver.configure.nrMmwMeas.multiEval.result.set_se_mask(enable = False) \n
		Enables or disables the evaluation of results in the multi-evaluation measurement. \n
			:param enable: OFF: Do not evaluate results ON: Evaluate results
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:SEMask {param}')

	def get_aclr(self) -> bool:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:ACLR \n
		Snippet: value: bool = driver.configure.nrMmwMeas.multiEval.result.get_aclr() \n
		Enables or disables the evaluation of results in the multi-evaluation measurement. \n
			:return: enable: OFF: Do not evaluate results ON: Evaluate results
		"""
		response = self._core.io.query_str('CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:ACLR?')
		return Conversions.str_to_bool(response)

	def set_aclr(self, enable: bool) -> None:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:ACLR \n
		Snippet: driver.configure.nrMmwMeas.multiEval.result.set_aclr(enable = False) \n
		Enables or disables the evaluation of results in the multi-evaluation measurement. \n
			:param enable: OFF: Do not evaluate results ON: Evaluate results
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:ACLR {param}')

	def get_pdynamics(self) -> bool:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:PDYNamics \n
		Snippet: value: bool = driver.configure.nrMmwMeas.multiEval.result.get_pdynamics() \n
		Enables or disables the evaluation of results in the multi-evaluation measurement. \n
			:return: enable: OFF: Do not evaluate results ON: Evaluate results
		"""
		response = self._core.io.query_str('CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:PDYNamics?')
		return Conversions.str_to_bool(response)

	def set_pdynamics(self, enable: bool) -> None:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:PDYNamics \n
		Snippet: driver.configure.nrMmwMeas.multiEval.result.set_pdynamics(enable = False) \n
		Enables or disables the evaluation of results in the multi-evaluation measurement. \n
			:param enable: OFF: Do not evaluate results ON: Evaluate results
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:PDYNamics {param}')

	def get_pmonitor(self) -> bool:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:PMONitor \n
		Snippet: value: bool = driver.configure.nrMmwMeas.multiEval.result.get_pmonitor() \n
		Enables or disables the evaluation of results in the multi-evaluation measurement. \n
			:return: enable: OFF: Do not evaluate results ON: Evaluate results
		"""
		response = self._core.io.query_str('CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:PMONitor?')
		return Conversions.str_to_bool(response)

	def set_pmonitor(self, enable: bool) -> None:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:PMONitor \n
		Snippet: driver.configure.nrMmwMeas.multiEval.result.set_pmonitor(enable = False) \n
		Enables or disables the evaluation of results in the multi-evaluation measurement. \n
			:param enable: OFF: Do not evaluate results ON: Evaluate results
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:PMONitor {param}')

	def get_merror(self) -> bool:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:MERRor \n
		Snippet: value: bool = driver.configure.nrMmwMeas.multiEval.result.get_merror() \n
		Enables or disables the evaluation of results in the multi-evaluation measurement.
			Table Header: Mnemonic / Description \n
			- EVMagnitude / Error vector magnitude
			- MERRor / Magnitude error
			- IEMissions / Inband emissions
			- ESFLatness / Equalizer spectrum flatness
			- EVMC / EVM vs. subcarrier
			- PERRor / Phase error
			- IQ / I/Q constellation diagram
			-  \n
			:return: enable: OFF: Do not evaluate results ON: Evaluate results
		"""
		response = self._core.io.query_str('CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:MERRor?')
		return Conversions.str_to_bool(response)

	def set_merror(self, enable: bool) -> None:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:MERRor \n
		Snippet: driver.configure.nrMmwMeas.multiEval.result.set_merror(enable = False) \n
		Enables or disables the evaluation of results in the multi-evaluation measurement.
			Table Header: Mnemonic / Description \n
			- EVMagnitude / Error vector magnitude
			- MERRor / Magnitude error
			- IEMissions / Inband emissions
			- ESFLatness / Equalizer spectrum flatness
			- EVMC / EVM vs. subcarrier
			- PERRor / Phase error
			- IQ / I/Q constellation diagram
			-  \n
			:param enable: OFF: Do not evaluate results ON: Evaluate results
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:MERRor {param}')

	def get_perror(self) -> bool:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:PERRor \n
		Snippet: value: bool = driver.configure.nrMmwMeas.multiEval.result.get_perror() \n
		Enables or disables the evaluation of results in the multi-evaluation measurement.
			Table Header: Mnemonic / Description \n
			- EVMagnitude / Error vector magnitude
			- MERRor / Magnitude error
			- IEMissions / Inband emissions
			- ESFLatness / Equalizer spectrum flatness
			- EVMC / EVM vs. subcarrier
			- PERRor / Phase error
			- IQ / I/Q constellation diagram
			-  \n
			:return: enable: OFF: Do not evaluate results ON: Evaluate results
		"""
		response = self._core.io.query_str('CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:PERRor?')
		return Conversions.str_to_bool(response)

	def set_perror(self, enable: bool) -> None:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:PERRor \n
		Snippet: driver.configure.nrMmwMeas.multiEval.result.set_perror(enable = False) \n
		Enables or disables the evaluation of results in the multi-evaluation measurement.
			Table Header: Mnemonic / Description \n
			- EVMagnitude / Error vector magnitude
			- MERRor / Magnitude error
			- IEMissions / Inband emissions
			- ESFLatness / Equalizer spectrum flatness
			- EVMC / EVM vs. subcarrier
			- PERRor / Phase error
			- IQ / I/Q constellation diagram
			-  \n
			:param enable: OFF: Do not evaluate results ON: Evaluate results
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:PERRor {param}')

	def get_evmc(self) -> bool:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:EVMC \n
		Snippet: value: bool = driver.configure.nrMmwMeas.multiEval.result.get_evmc() \n
		Enables or disables the evaluation of results in the multi-evaluation measurement.
			Table Header: Mnemonic / Description \n
			- EVMagnitude / Error vector magnitude
			- MERRor / Magnitude error
			- IEMissions / Inband emissions
			- ESFLatness / Equalizer spectrum flatness
			- EVMC / EVM vs. subcarrier
			- PERRor / Phase error
			- IQ / I/Q constellation diagram
			-  \n
			:return: enable: OFF: Do not evaluate results ON: Evaluate results
		"""
		response = self._core.io.query_str('CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:EVMC?')
		return Conversions.str_to_bool(response)

	def set_evmc(self, enable: bool) -> None:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:EVMC \n
		Snippet: driver.configure.nrMmwMeas.multiEval.result.set_evmc(enable = False) \n
		Enables or disables the evaluation of results in the multi-evaluation measurement.
			Table Header: Mnemonic / Description \n
			- EVMagnitude / Error vector magnitude
			- MERRor / Magnitude error
			- IEMissions / Inband emissions
			- ESFLatness / Equalizer spectrum flatness
			- EVMC / EVM vs. subcarrier
			- PERRor / Phase error
			- IQ / I/Q constellation diagram
			-  \n
			:param enable: OFF: Do not evaluate results ON: Evaluate results
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:EVMC {param}')

	def get_iemissions(self) -> bool:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:IEMissions \n
		Snippet: value: bool = driver.configure.nrMmwMeas.multiEval.result.get_iemissions() \n
		Enables or disables the evaluation of results in the multi-evaluation measurement.
			Table Header: Mnemonic / Description \n
			- EVMagnitude / Error vector magnitude
			- MERRor / Magnitude error
			- IEMissions / Inband emissions
			- ESFLatness / Equalizer spectrum flatness
			- EVMC / EVM vs. subcarrier
			- PERRor / Phase error
			- IQ / I/Q constellation diagram
			-  \n
			:return: enable: OFF: Do not evaluate results ON: Evaluate results
		"""
		response = self._core.io.query_str('CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:IEMissions?')
		return Conversions.str_to_bool(response)

	def set_iemissions(self, enable: bool) -> None:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:IEMissions \n
		Snippet: driver.configure.nrMmwMeas.multiEval.result.set_iemissions(enable = False) \n
		Enables or disables the evaluation of results in the multi-evaluation measurement.
			Table Header: Mnemonic / Description \n
			- EVMagnitude / Error vector magnitude
			- MERRor / Magnitude error
			- IEMissions / Inband emissions
			- ESFLatness / Equalizer spectrum flatness
			- EVMC / EVM vs. subcarrier
			- PERRor / Phase error
			- IQ / I/Q constellation diagram
			-  \n
			:param enable: OFF: Do not evaluate results ON: Evaluate results
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:IEMissions {param}')

	def get_es_flatness(self) -> bool:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:ESFLatness \n
		Snippet: value: bool = driver.configure.nrMmwMeas.multiEval.result.get_es_flatness() \n
		Enables or disables the evaluation of results in the multi-evaluation measurement.
			Table Header: Mnemonic / Description \n
			- EVMagnitude / Error vector magnitude
			- MERRor / Magnitude error
			- IEMissions / Inband emissions
			- ESFLatness / Equalizer spectrum flatness
			- EVMC / EVM vs. subcarrier
			- PERRor / Phase error
			- IQ / I/Q constellation diagram
			-  \n
			:return: enable: OFF: Do not evaluate results ON: Evaluate results
		"""
		response = self._core.io.query_str('CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:ESFLatness?')
		return Conversions.str_to_bool(response)

	def set_es_flatness(self, enable: bool) -> None:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:ESFLatness \n
		Snippet: driver.configure.nrMmwMeas.multiEval.result.set_es_flatness(enable = False) \n
		Enables or disables the evaluation of results in the multi-evaluation measurement.
			Table Header: Mnemonic / Description \n
			- EVMagnitude / Error vector magnitude
			- MERRor / Magnitude error
			- IEMissions / Inband emissions
			- ESFLatness / Equalizer spectrum flatness
			- EVMC / EVM vs. subcarrier
			- PERRor / Phase error
			- IQ / I/Q constellation diagram
			-  \n
			:param enable: OFF: Do not evaluate results ON: Evaluate results
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:ESFLatness {param}')

	def get_iq(self) -> bool:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:IQ \n
		Snippet: value: bool = driver.configure.nrMmwMeas.multiEval.result.get_iq() \n
		Enables or disables the evaluation of results in the multi-evaluation measurement.
			Table Header: Mnemonic / Description \n
			- EVMagnitude / Error vector magnitude
			- MERRor / Magnitude error
			- IEMissions / Inband emissions
			- ESFLatness / Equalizer spectrum flatness
			- EVMC / EVM vs. subcarrier
			- PERRor / Phase error
			- IQ / I/Q constellation diagram
			-  \n
			:return: enable: OFF: Do not evaluate results ON: Evaluate results
		"""
		response = self._core.io.query_str('CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:IQ?')
		return Conversions.str_to_bool(response)

	def set_iq(self, enable: bool) -> None:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:IQ \n
		Snippet: driver.configure.nrMmwMeas.multiEval.result.set_iq(enable = False) \n
		Enables or disables the evaluation of results in the multi-evaluation measurement.
			Table Header: Mnemonic / Description \n
			- EVMagnitude / Error vector magnitude
			- MERRor / Magnitude error
			- IEMissions / Inband emissions
			- ESFLatness / Equalizer spectrum flatness
			- EVMC / EVM vs. subcarrier
			- PERRor / Phase error
			- IQ / I/Q constellation diagram
			-  \n
			:param enable: OFF: Do not evaluate results ON: Evaluate results
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:IQ {param}')

	def get_txm(self) -> bool:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:TXM \n
		Snippet: value: bool = driver.configure.nrMmwMeas.multiEval.result.get_txm() \n
		Enables or disables the evaluation of results in the multi-evaluation measurement. \n
			:return: enable: OFF: Do not evaluate results ON: Evaluate results
		"""
		response = self._core.io.query_str('CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:TXM?')
		return Conversions.str_to_bool(response)

	def set_txm(self, enable: bool) -> None:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:TXM \n
		Snippet: driver.configure.nrMmwMeas.multiEval.result.set_txm(enable = False) \n
		Enables or disables the evaluation of results in the multi-evaluation measurement. \n
			:param enable: OFF: Do not evaluate results ON: Evaluate results
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:TXM {param}')

	# noinspection PyTypeChecker
	class AllStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Evm: bool: Error vector magnitude OFF: Do not evaluate results ON: Evaluate results
			- Magnitude_Error: bool: No parameter help available
			- Phase_Error: bool: No parameter help available
			- Inband_Emissions: bool: No parameter help available
			- Evmversus_C: bool: No parameter help available
			- Iq: bool: No parameter help available
			- Equ_Spec_Flatness: bool: No parameter help available
			- Tx_Measurement: bool: No parameter help available
			- Spec_Em_Mask: bool: No parameter help available
			- Aclr: bool: No parameter help available
			- Power_Monitor: bool: No parameter help available
			- Power_Dynamics: bool: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Evm'),
			ArgStruct.scalar_bool('Magnitude_Error'),
			ArgStruct.scalar_bool('Phase_Error'),
			ArgStruct.scalar_bool('Inband_Emissions'),
			ArgStruct.scalar_bool('Evmversus_C'),
			ArgStruct.scalar_bool('Iq'),
			ArgStruct.scalar_bool('Equ_Spec_Flatness'),
			ArgStruct.scalar_bool('Tx_Measurement'),
			ArgStruct.scalar_bool('Spec_Em_Mask'),
			ArgStruct.scalar_bool('Aclr'),
			ArgStruct.scalar_bool('Power_Monitor'),
			ArgStruct.scalar_bool('Power_Dynamics')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Evm: bool = None
			self.Magnitude_Error: bool = None
			self.Phase_Error: bool = None
			self.Inband_Emissions: bool = None
			self.Evmversus_C: bool = None
			self.Iq: bool = None
			self.Equ_Spec_Flatness: bool = None
			self.Tx_Measurement: bool = None
			self.Spec_Em_Mask: bool = None
			self.Aclr: bool = None
			self.Power_Monitor: bool = None
			self.Power_Dynamics: bool = None

	def get_all(self) -> AllStruct:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult[:ALL] \n
		Snippet: value: AllStruct = driver.configure.nrMmwMeas.multiEval.result.get_all() \n
		Enables or disables the evaluation of results in the multi-evaluation measurement. \n
			:return: structure: for return value, see the help for AllStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:ALL?', self.__class__.AllStruct())

	def set_all(self, value: AllStruct) -> None:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult[:ALL] \n
		Snippet: driver.configure.nrMmwMeas.multiEval.result.set_all(value = AllStruct()) \n
		Enables or disables the evaluation of results in the multi-evaluation measurement. \n
			:param value: see the help for AllStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:NRMMw:MEASurement<Instance>:MEValuation:RESult:ALL', value)

	def clone(self) -> 'Result':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Result(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Average:
	"""Average commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("average", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Nr_Neg: float: ACLR for the adjacent NR channel with lower frequency
			- Carrier: float: Power in the allocated NR channel
			- Nr_Pos: float: ACLR for the adjacent NR channel with higher frequency"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Nr_Neg'),
			ArgStruct.scalar_float('Carrier'),
			ArgStruct.scalar_float('Nr_Pos')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Nr_Neg: float = None
			self.Carrier: float = None
			self.Nr_Pos: float = None

	def read(self) -> ResultData:
		"""SCPI: READ:NRMMw:MEASurement<Instance>:MEValuation:ACLR:AVERage \n
		Snippet: value: ResultData = driver.nrMmwMeas.multiEval.aclr.average.read() \n
		Returns the relative ACLR values as displayed in the table below the ACLR diagram. The current and average values can be
		retrieved. See also 'Square Spectrum ACLR'. The values described below are returned by FETCh and READ commands. CALCulate
		commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:NRMMw:MEASurement<Instance>:MEValuation:ACLR:AVERage?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:NRMMw:MEASurement<Instance>:MEValuation:ACLR:AVERage \n
		Snippet: value: ResultData = driver.nrMmwMeas.multiEval.aclr.average.fetch() \n
		Returns the relative ACLR values as displayed in the table below the ACLR diagram. The current and average values can be
		retrieved. See also 'Square Spectrum ACLR'. The values described below are returned by FETCh and READ commands. CALCulate
		commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:NRMMw:MEASurement<Instance>:MEValuation:ACLR:AVERage?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Nr_Neg: enums.ResultStatus2: ACLR for the adjacent NR channel with lower frequency
			- Carrier: enums.ResultStatus2: Power in the allocated NR channel
			- Nr_Pos: enums.ResultStatus2: ACLR for the adjacent NR channel with higher frequency"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_enum('Nr_Neg', enums.ResultStatus2),
			ArgStruct.scalar_enum('Carrier', enums.ResultStatus2),
			ArgStruct.scalar_enum('Nr_Pos', enums.ResultStatus2)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Nr_Neg: enums.ResultStatus2 = None
			self.Carrier: enums.ResultStatus2 = None
			self.Nr_Pos: enums.ResultStatus2 = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:NRMMw:MEASurement<Instance>:MEValuation:ACLR:AVERage \n
		Snippet: value: CalculateStruct = driver.nrMmwMeas.multiEval.aclr.average.calculate() \n
		Returns the relative ACLR values as displayed in the table below the ACLR diagram. The current and average values can be
		retrieved. See also 'Square Spectrum ACLR'. The values described below are returned by FETCh and READ commands. CALCulate
		commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:NRMMw:MEASurement<Instance>:MEValuation:ACLR:AVERage?', self.__class__.CalculateStruct())

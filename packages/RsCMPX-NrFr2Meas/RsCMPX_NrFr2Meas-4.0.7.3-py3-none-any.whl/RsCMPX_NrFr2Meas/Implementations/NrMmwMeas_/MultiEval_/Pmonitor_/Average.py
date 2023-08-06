from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Average:
	"""Average commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("average", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: No parameter help available
			- Out_Of_Tolerance: int: No parameter help available
			- Tx_Power: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_float('Tx_Power')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tolerance: int = None
			self.Tx_Power: float = None

	def read(self) -> ResultData:
		"""SCPI: READ:NRMMw:MEASurement<Instance>:MEValuation:PMONitor:AVERage \n
		Snippet: value: ResultData = driver.nrMmwMeas.multiEval.pmonitor.average.read() \n
		No command help available \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:NRMMw:MEASurement<Instance>:MEValuation:PMONitor:AVERage?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:NRMMw:MEASurement<Instance>:MEValuation:PMONitor:AVERage \n
		Snippet: value: ResultData = driver.nrMmwMeas.multiEval.pmonitor.average.fetch() \n
		No command help available \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:NRMMw:MEASurement<Instance>:MEValuation:PMONitor:AVERage?', self.__class__.ResultData())

from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pmonitor:
	"""Pmonitor commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pmonitor", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:NRMMw:MEASurement<Instance>:MEValuation:TRACe:PMONitor \n
		Snippet: value: List[float] = driver.nrMmwMeas.multiEval.trace.pmonitor.fetch() \n
		Returns the power monitor results. \n
		Suppressed linked return values: reliability \n
			:return: power: Comma-separated list of power values, one value per slot"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:NRMMw:MEASurement<Instance>:MEValuation:TRACe:PMONitor?', suppressed)
		return response

	def read(self) -> List[float]:
		"""SCPI: READ:NRMMw:MEASurement<Instance>:MEValuation:TRACe:PMONitor \n
		Snippet: value: List[float] = driver.nrMmwMeas.multiEval.trace.pmonitor.read() \n
		Returns the power monitor results. \n
		Suppressed linked return values: reliability \n
			:return: power: Comma-separated list of power values, one value per slot"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:NRMMw:MEASurement<Instance>:MEValuation:TRACe:PMONitor?', suppressed)
		return response

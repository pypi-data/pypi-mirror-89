from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .........Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Extreme:
	"""Extreme commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("extreme", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:NRMMw:MEASurement<Instance>:MEValuation:LIST:MODulation:EVM:PEAK:LOW:EXTReme \n
		Snippet: value: List[float] = driver.nrMmwMeas.multiEval.listPy.modulation.evm.peak.low.extreme.fetch() \n
		Return error vector magnitude peak values for low and high EVM window position, for all measured list mode segments. The
		values described below are returned by FETCh commands. CALCulate commands return limit check results instead, one value
		for each result listed below. \n
		Suppressed linked return values: reliability \n
			:return: evmpeak_low: Comma-separated list of values, one per measured segment"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:NRMMw:MEASurement<Instance>:MEValuation:LIST:MODulation:EVM:PEAK:LOW:EXTReme?', suppressed)
		return response

	def calculate(self) -> List[float]:
		"""SCPI: CALCulate:NRMMw:MEASurement<Instance>:MEValuation:LIST:MODulation:EVM:PEAK:LOW:EXTReme \n
		Snippet: value: List[float] = driver.nrMmwMeas.multiEval.listPy.modulation.evm.peak.low.extreme.calculate() \n
		Return error vector magnitude peak values for low and high EVM window position, for all measured list mode segments. The
		values described below are returned by FETCh commands. CALCulate commands return limit check results instead, one value
		for each result listed below. \n
		Suppressed linked return values: reliability \n
			:return: evmpeak_low: Comma-separated list of values, one per measured segment"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'CALCulate:NRMMw:MEASurement<Instance>:MEValuation:LIST:MODulation:EVM:PEAK:LOW:EXTReme?', suppressed)
		return response

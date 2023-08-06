from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Positiv:
	"""Positiv commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("positiv", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Out_Of_Tolerance: int: Out of tolerance result, i.e. percentage of measurement intervals of the statistic count for spectrum emission measurements exceeding the specified spectrum emission mask limits.
			- Margin_Pow_Curr_Pos: List[float]: Comma-separated list of 12 trace values, one value per emission mask area"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct('Margin_Pow_Curr_Pos', DataType.FloatList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tolerance: int = None
			self.Margin_Pow_Curr_Pos: List[float] = None

	def fetch(self) -> FetchStruct:
		"""SCPI: FETCh:NRMMw:MEASurement<Instance>:MEValuation:SEMask:MARGin:CURRent:POWer:POSitiv \n
		Snippet: value: FetchStruct = driver.nrMmwMeas.multiEval.seMask.margin.current.power.positiv.fetch() \n
		Returns the spectrum emission trace values at the limit line margin positions of the emission mask areas. The individual
		commands provide results for the CURRent, AVERage and maximum traces (resulting in MINimum margins) . There are results
		for NEGative and POSitive offset frequencies. For inactive areas, NCAP is returned. \n
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		return self._core.io.query_struct(f'FETCh:NRMMw:MEASurement<Instance>:MEValuation:SEMask:MARGin:CURRent:POWer:POSitiv?', self.__class__.FetchStruct())

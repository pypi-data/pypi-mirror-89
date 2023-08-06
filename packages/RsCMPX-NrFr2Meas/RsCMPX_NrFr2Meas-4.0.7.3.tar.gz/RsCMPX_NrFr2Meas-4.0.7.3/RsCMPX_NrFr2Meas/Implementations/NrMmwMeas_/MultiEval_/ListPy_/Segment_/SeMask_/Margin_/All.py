from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class All:
	"""All commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("all", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Seg_Reliability: int: Reliability indicator for the segment
			- Statist_Expired: int: Reached statistical length in slots
			- Out_Of_Tolerance: int: Percentage of measured subframes with failed limit check
			- Margin_Curr_Neg: List[float]: No parameter help available
			- Margin_Curr_Pos: List[float]: No parameter help available
			- Margin_Avg_Neg: List[float]: No parameter help available
			- Margin_Avg_Pos: List[float]: No parameter help available
			- Margin_Min_Neg: List[float]: No parameter help available
			- Margin_Min_Pos: List[float]: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Seg_Reliability'),
			ArgStruct.scalar_int('Statist_Expired'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct('Margin_Curr_Neg', DataType.FloatList, None, False, False, 12),
			ArgStruct('Margin_Curr_Pos', DataType.FloatList, None, False, False, 12),
			ArgStruct('Margin_Avg_Neg', DataType.FloatList, None, False, False, 12),
			ArgStruct('Margin_Avg_Pos', DataType.FloatList, None, False, False, 12),
			ArgStruct('Margin_Min_Neg', DataType.FloatList, None, False, False, 12),
			ArgStruct('Margin_Min_Pos', DataType.FloatList, None, False, False, 12)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Seg_Reliability: int = None
			self.Statist_Expired: int = None
			self.Out_Of_Tolerance: int = None
			self.Margin_Curr_Neg: List[float] = None
			self.Margin_Curr_Pos: List[float] = None
			self.Margin_Avg_Neg: List[float] = None
			self.Margin_Avg_Pos: List[float] = None
			self.Margin_Min_Neg: List[float] = None
			self.Margin_Min_Pos: List[float] = None

	def fetch(self, sEGMent=repcap.SEGMent.Default) -> FetchStruct:
		"""SCPI: FETCh:NRMMw:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>:SEMask:MARGin:ALL \n
		Snippet: value: FetchStruct = driver.nrMmwMeas.multiEval.listPy.segment.seMask.margin.all.fetch(sEGMent = repcap.SEGMent.Default) \n
		Return limit line margin values, i.e. vertical distances between the spectrum emission mask limit line and a trace, for
		segment <no> in list mode. \n
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		sEGMent_cmd_val = self._base.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		return self._core.io.query_struct(f'FETCh:NRMMw:MEASurement<Instance>:MEValuation:LIST:SEGMent{sEGMent_cmd_val}:SEMask:MARGin:ALL?', self.__class__.FetchStruct())

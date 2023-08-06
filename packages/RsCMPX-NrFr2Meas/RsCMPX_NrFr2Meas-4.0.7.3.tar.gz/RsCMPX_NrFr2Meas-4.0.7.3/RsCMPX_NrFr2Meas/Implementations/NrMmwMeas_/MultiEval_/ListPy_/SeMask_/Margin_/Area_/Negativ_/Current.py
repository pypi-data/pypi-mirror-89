from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.Types import DataType
from .........Internal.StructBase import StructBase
from .........Internal.ArgStruct import ArgStruct
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("current", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Margin_Curr_Neg_X: List[float]: No parameter help available
			- Margin_Curr_Neg_Y: List[float]: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct('Margin_Curr_Neg_X', DataType.FloatList, None, False, True, 1),
			ArgStruct('Margin_Curr_Neg_Y', DataType.FloatList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Margin_Curr_Neg_X: List[float] = None
			self.Margin_Curr_Neg_Y: List[float] = None

	def fetch(self, area=repcap.Area.Default) -> FetchStruct:
		"""SCPI: FETCh:NRMMw:MEASurement<Instance>:MEValuation:LIST:SEMask:MARGin:AREA<nr>:NEGativ:CURRent \n
		Snippet: value: FetchStruct = driver.nrMmwMeas.multiEval.listPy.seMask.margin.area.negativ.current.fetch(area = repcap.Area.Default) \n
		Return spectrum emission mask margin positions for all measured list mode segments. The individual commands provide
		results for the CURRent, AVERage and maximum traces (resulting in MINimum margins) for NEGative and POSitive offset
		frequencies. The results are returned as pairs per segment: <Reliability>, {<MarginPosX>, <MarginPosY>}seg 1,
		{<MarginPosX>, <MarginPosY>}seg 2, ... \n
			:param area: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Area')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		area_cmd_val = self._base.get_repcap_cmd_value(area, repcap.Area)
		return self._core.io.query_struct(f'FETCh:NRMMw:MEASurement<Instance>:MEValuation:LIST:SEMask:MARGin:AREA{area_cmd_val}:NEGativ:CURRent?', self.__class__.FetchStruct())

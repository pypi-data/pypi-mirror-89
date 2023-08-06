from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ........Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("current", core, parent)

	def fetch(self) -> List[int]:
		"""SCPI: FETCh:NRMMw:MEASurement<Instance>:MEValuation:LIST:IEMission:MARGin:RBINdex:CURRent \n
		Snippet: value: List[int] = driver.nrMmwMeas.multiEval.listPy.iemission.margin.rbIndex.current.fetch() \n
		Return resource block indices of the inband emission measurement for all measured list mode segments. At these RB indices,
		the CURRent and EXTReme margins have been detected. The results are returned as triplets per segment: <Reliability>,
		{<RBindex>, <IQImage>, <CarrLeakage>}seg 1, {<RBindex>, <IQImage>, <CarrLeakage>}seg 2, ... \n
		Suppressed linked return values: reliability \n
			:return: rb_index: Resource block index for the general margin (at non-allocated RBs)"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_int_list_suppressed(f'FETCh:NRMMw:MEASurement<Instance>:MEValuation:LIST:IEMission:MARGin:RBINdex:CURRent?', suppressed)
		return response

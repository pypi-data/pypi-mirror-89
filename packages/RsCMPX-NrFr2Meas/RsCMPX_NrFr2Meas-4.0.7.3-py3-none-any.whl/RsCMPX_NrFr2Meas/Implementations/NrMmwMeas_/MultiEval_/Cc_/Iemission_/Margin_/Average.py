from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Average:
	"""Average commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("average", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Out_Of_Tolerance: int: Out of tolerance result, i.e. percentage of measurement intervals of the statistic count for modulation measurements exceeding the specified modulation limits.
			- General: float: Margin over all non-allocated RBs (scope of general limit component)
			- Iq_Image: float: Margin at image frequencies of allocated RBs (scope of IQ image limit component)
			- Carr_Leakage: float: Margin at the carrier frequency (scope of IQ offset limit component)"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_float('General'),
			ArgStruct.scalar_float('Iq_Image'),
			ArgStruct.scalar_float('Carr_Leakage')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tolerance: int = None
			self.General: float = None
			self.Iq_Image: float = None
			self.Carr_Leakage: float = None

	def fetch(self, carrierComponent=repcap.CarrierComponent.Default) -> FetchStruct:
		"""SCPI: FETCh:NRMMw:MEASurement<Instance>:MEValuation[:CC<no>]:IEMission:MARGin:AVERage \n
		Snippet: value: FetchStruct = driver.nrMmwMeas.multiEval.cc.iemission.margin.average.fetch(carrierComponent = repcap.CarrierComponent.Default) \n
		Return the limit line margin results for carrier <no>. The CURRent margin indicates the minimum (vertical) distance
		between the inband emissions limit line and the current trace. A negative result indicates that the limit is exceeded.
		The AVERage, EXTReme and SDEViation values are calculated from the current margins. The margin results cannot be
		displayed at the GUI. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		return self._core.io.query_struct(f'FETCh:NRMMw:MEASurement<Instance>:MEValuation:CC{carrierComponent_cmd_val}:IEMission:MARGin:AVERage?', self.__class__.FetchStruct())

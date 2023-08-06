from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Extreme:
	"""Extreme commands group definition. 3 total commands, 2 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("extreme", core, parent)

	@property
	def rbIndex(self):
		"""rbIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbIndex'):
			from .Extreme_.RbIndex import RbIndex
			self._rbIndex = RbIndex(self._core, self._base)
		return self._rbIndex

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Extreme_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Seg_Reliability: int: Reliability indicator for the segment
			- Statist_Expired: int: Reached statistical length in slots
			- Out_Of_Tolerance: int: Percentage of measured subframes with failed limit check
			- General: float: Margin over all non-allocated RBs (scope of general limit component)
			- Iq_Image: float: Margin at image frequencies of allocated RBs (scope of IQ image limit component)
			- Carr_Leakage: float: Margin at the carrier frequency (scope of IQ offset limit component)"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Seg_Reliability'),
			ArgStruct.scalar_int('Statist_Expired'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_float('General'),
			ArgStruct.scalar_float('Iq_Image'),
			ArgStruct.scalar_float('Carr_Leakage')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Seg_Reliability: int = None
			self.Statist_Expired: int = None
			self.Out_Of_Tolerance: int = None
			self.General: float = None
			self.Iq_Image: float = None
			self.Carr_Leakage: float = None

	def fetch(self, sEGMent=repcap.SEGMent.Default) -> FetchStruct:
		"""SCPI: FETCh:NRMMw:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>:IEMission:MARGin:EXTReme \n
		Snippet: value: FetchStruct = driver.nrMmwMeas.multiEval.listPy.segment.iemission.margin.extreme.fetch(sEGMent = repcap.SEGMent.Default) \n
		Return the inband emission limit line margin results for segment <no> in list mode. The CURRent margins indicate the
		minimum (vertical) distance between the limit line and the current trace. A negative result indicates that the limit is
		exceeded. The AVERage, EXTReme and SDEViation values are calculated from the current margins. \n
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		sEGMent_cmd_val = self._base.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		return self._core.io.query_struct(f'FETCh:NRMMw:MEASurement<Instance>:MEValuation:LIST:SEGMent{sEGMent_cmd_val}:IEMission:MARGin:EXTReme?', self.__class__.FetchStruct())

	def clone(self) -> 'Extreme':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Extreme(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

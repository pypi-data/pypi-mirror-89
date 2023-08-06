from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Extreme:
	"""Extreme commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("extreme", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Out_Of_Tolerance: int: Out of tolerance result, i.e. percentage of measurement intervals of the statistic count for modulation measurements exceeding the specified modulation limits.
			- Ripple_1: float: Max (range 1) - min (range 1)
			- Ripple_2: float: Max (range 2) - min (range 2)
			- Max_R_1_Min_R_2: float: Max (range 1) - min (range 2)
			- Max_R_2_Min_R_1: float: Max (range 2) - min (range 1)
			- Min_R_1: float: Min (range 1)
			- Max_R_1: float: Max (range 1)
			- Min_R_2: float: Min (range 2)
			- Max_R_2: float: Max (range 2)"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_float('Ripple_1'),
			ArgStruct.scalar_float('Ripple_2'),
			ArgStruct.scalar_float('Max_R_1_Min_R_2'),
			ArgStruct.scalar_float('Max_R_2_Min_R_1'),
			ArgStruct.scalar_float('Min_R_1'),
			ArgStruct.scalar_float('Max_R_1'),
			ArgStruct.scalar_float('Min_R_2'),
			ArgStruct.scalar_float('Max_R_2')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tolerance: int = None
			self.Ripple_1: float = None
			self.Ripple_2: float = None
			self.Max_R_1_Min_R_2: float = None
			self.Max_R_2_Min_R_1: float = None
			self.Min_R_1: float = None
			self.Max_R_1: float = None
			self.Min_R_2: float = None
			self.Max_R_2: float = None

	def read(self, carrierComponent=repcap.CarrierComponent.Default) -> ResultData:
		"""SCPI: READ:NRMMw:MEASurement<Instance>:MEValuation[:CC<no>]:ESFLatness:EXTReme \n
		Snippet: value: ResultData = driver.nrMmwMeas.multiEval.cc.esFlatness.extreme.read(carrierComponent = repcap.CarrierComponent.Default) \n
		Return current, average, extreme and standard deviation single value results of the equalizer spectrum flatness
		measurement, for carrier <no>. See also 'Equalizer Spectrum Flatness Limits'. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: structure: for return value, see the help for ResultData structure arguments."""
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		return self._core.io.query_struct(f'READ:NRMMw:MEASurement<Instance>:MEValuation:CC{carrierComponent_cmd_val}:ESFLatness:EXTReme?', self.__class__.ResultData())

	def fetch(self, carrierComponent=repcap.CarrierComponent.Default) -> ResultData:
		"""SCPI: FETCh:NRMMw:MEASurement<Instance>:MEValuation[:CC<no>]:ESFLatness:EXTReme \n
		Snippet: value: ResultData = driver.nrMmwMeas.multiEval.cc.esFlatness.extreme.fetch(carrierComponent = repcap.CarrierComponent.Default) \n
		Return current, average, extreme and standard deviation single value results of the equalizer spectrum flatness
		measurement, for carrier <no>. See also 'Equalizer Spectrum Flatness Limits'. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: structure: for return value, see the help for ResultData structure arguments."""
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		return self._core.io.query_struct(f'FETCh:NRMMw:MEASurement<Instance>:MEValuation:CC{carrierComponent_cmd_val}:ESFLatness:EXTReme?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Out_Of_Tolerance: int: Out of tolerance result, i.e. percentage of measurement intervals of the statistic count for modulation measurements exceeding the specified modulation limits.
			- Ripple_1: float: Limit check result for max (range 1) - min (range 1)
			- Ripple_2: float: Limit check result for max (range 2) - min (range 2)
			- Max_R_1_Min_R_2: float: Limit check result for max (range 1) - min (range 2)
			- Max_R_2_Min_R_1: float: Limit check result for max (range 2) - min (range 1)"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_float('Ripple_1'),
			ArgStruct.scalar_float('Ripple_2'),
			ArgStruct.scalar_float('Max_R_1_Min_R_2'),
			ArgStruct.scalar_float('Max_R_2_Min_R_1')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tolerance: int = None
			self.Ripple_1: float = None
			self.Ripple_2: float = None
			self.Max_R_1_Min_R_2: float = None
			self.Max_R_2_Min_R_1: float = None

	def calculate(self, carrierComponent=repcap.CarrierComponent.Default) -> CalculateStruct:
		"""SCPI: CALCulate:NRMMw:MEASurement<Instance>:MEValuation[:CC<no>]:ESFLatness:EXTReme \n
		Snippet: value: CalculateStruct = driver.nrMmwMeas.multiEval.cc.esFlatness.extreme.calculate(carrierComponent = repcap.CarrierComponent.Default) \n
		Return current, average and extreme limit check results for the equalizer spectrum flatness measurement, for carrier <no>.
		See also 'Equalizer Spectrum Flatness Limits'. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		return self._core.io.query_struct(f'CALCulate:NRMMw:MEASurement<Instance>:MEValuation:CC{carrierComponent_cmd_val}:ESFLatness:EXTReme?', self.__class__.CalculateStruct())

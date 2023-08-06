from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScIndex:
	"""ScIndex commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scIndex", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Out_Of_Tolerance: int: Out of tolerance result, i.e. percentage of measurement intervals of the statistic count for modulation measurements exceeding the specified modulation limits.
			- Maximum_1: int: SC index of Max (Range 1)
			- Minimum_1: int: SC index of Min (Range 1)
			- Maximum_2: int: SC index of Max (Range 2)
			- Minimum_2: int: SC index of Min (Range 2)"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_int('Maximum_1'),
			ArgStruct.scalar_int('Minimum_1'),
			ArgStruct.scalar_int('Maximum_2'),
			ArgStruct.scalar_int('Minimum_2')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tolerance: int = None
			self.Maximum_1: int = None
			self.Minimum_1: int = None
			self.Maximum_2: int = None
			self.Minimum_2: int = None

	def fetch(self, carrierComponent=repcap.CarrierComponent.Default) -> FetchStruct:
		"""SCPI: FETCh:NRMMw:MEASurement<Instance>:MEValuation[:CC<no>]:ESFLatness:CURRent:SCINdex \n
		Snippet: value: FetchStruct = driver.nrMmwMeas.multiEval.cc.esFlatness.current.scIndex.fetch(carrierComponent = repcap.CarrierComponent.Default) \n
		Returns subcarrier indices of the equalizer spectrum flatness measurement for carrier <no>. At these SC indices, the
		current minimum and maximum power of the equalizer coefficients have been detected within range 1 and range 2. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		return self._core.io.query_struct(f'FETCh:NRMMw:MEASurement<Instance>:MEValuation:CC{carrierComponent_cmd_val}:ESFLatness:CURRent:SCINdex?', self.__class__.FetchStruct())

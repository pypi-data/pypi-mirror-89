from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BwPart:
	"""BwPart commands group definition. 4 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bwPart", core, parent)

	@property
	def pusch(self):
		"""pusch commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_pusch'):
			from .BwPart_.Pusch import Pusch
			self._pusch = Pusch(self._core, self._base)
		return self._pusch

	def set(self, bwp: enums.BandwidthPart, sc_spacing: enums.ScSpacing, cyclic_prefix: enums.CyclicPrefix, number_rb: int, start_rb: int, carrierComponent=repcap.CarrierComponent.Default) -> None:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>[:CC<no>]:BWPart \n
		Snippet: driver.configure.nrMmwMeas.cc.bwPart.set(bwp = enums.BandwidthPart.BWP0, sc_spacing = enums.ScSpacing.S120k, cyclic_prefix = enums.CyclicPrefix.EXTended, number_rb = 1, start_rb = 1, carrierComponent = repcap.CarrierComponent.Default) \n
		Configures basic properties of the <BWP> on carrier <no>. For dependencies of the RB ranges, see 'Resource Elements,
		Grids and Blocks'. \n
			:param bwp: No help available
			:param sc_spacing: Subcarrier spacing 60 kHz, 120 kHz.
			:param cyclic_prefix: Only normal CP is supported.
			:param number_rb: Number of RBs in the bandwidth part.
			:param start_rb: Index of the first RB in the bandwidth part.
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('bwp', bwp, DataType.Enum), ArgSingle('sc_spacing', sc_spacing, DataType.Enum), ArgSingle('cyclic_prefix', cyclic_prefix, DataType.Enum), ArgSingle('number_rb', number_rb, DataType.Integer), ArgSingle('start_rb', start_rb, DataType.Integer))
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		self._core.io.write(f'CONFigure:NRMMw:MEASurement<Instance>:CC{carrierComponent_cmd_val}:BWPart {param}'.rstrip())

	# noinspection PyTypeChecker
	class GetStruct(StructBase):
		"""Response structure. Fields: \n
			- Sc_Spacing: enums.ScSpacing: Subcarrier spacing 60 kHz, 120 kHz.
			- Cyclic_Prefix: enums.CyclicPrefix: Only normal CP is supported.
			- Number_Rb: int: Number of RBs in the bandwidth part.
			- Start_Rb: int: Index of the first RB in the bandwidth part."""
		__meta_args_list = [
			ArgStruct.scalar_enum('Sc_Spacing', enums.ScSpacing),
			ArgStruct.scalar_enum('Cyclic_Prefix', enums.CyclicPrefix),
			ArgStruct.scalar_int('Number_Rb'),
			ArgStruct.scalar_int('Start_Rb')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Sc_Spacing: enums.ScSpacing = None
			self.Cyclic_Prefix: enums.CyclicPrefix = None
			self.Number_Rb: int = None
			self.Start_Rb: int = None

	def get(self, bwp: enums.BandwidthPart, carrierComponent=repcap.CarrierComponent.Default) -> GetStruct:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>[:CC<no>]:BWPart \n
		Snippet: value: GetStruct = driver.configure.nrMmwMeas.cc.bwPart.get(bwp = enums.BandwidthPart.BWP0, carrierComponent = repcap.CarrierComponent.Default) \n
		Configures basic properties of the <BWP> on carrier <no>. For dependencies of the RB ranges, see 'Resource Elements,
		Grids and Blocks'. \n
			:param bwp: No help available
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		param = Conversions.enum_scalar_to_str(bwp, enums.BandwidthPart)
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		return self._core.io.query_struct(f'CONFigure:NRMMw:MEASurement<Instance>:CC{carrierComponent_cmd_val}:BWPart? {param}', self.__class__.GetStruct())

	def clone(self) -> 'BwPart':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BwPart(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

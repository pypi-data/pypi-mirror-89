from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.StructBase import StructBase
from .........Internal.ArgStruct import ArgStruct
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Blimits:
	"""Blimits commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: BandLimits, default value after init: BandLimits.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("blimits", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_bandLimits_get', 'repcap_bandLimits_set', repcap.BandLimits.Nr1)

	def repcap_bandLimits_set(self, enum_value: repcap.BandLimits) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to BandLimits.Default
		Default value after init: BandLimits.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_bandLimits_get(self) -> repcap.BandLimits:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	# noinspection PyTypeChecker
	class BlimitsStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Relative_Level: float or bool: Relative lower ACLR limit without test tolerance
			- Absolute_Level: float or bool: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_float_ext('Relative_Level'),
			ArgStruct.scalar_float_ext('Absolute_Level')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Relative_Level: float or bool = None
			self.Absolute_Level: float or bool = None

	def set(self, structure: BlimitsStruct, channelBw=repcap.ChannelBw.Default, bandLimits=repcap.BandLimits.Default) -> None:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>:MEValuation:LIMit:ACLR:NR:CBANdwidth<bw>:BLIMits<n> \n
		Snippet: driver.configure.nrMmwMeas.multiEval.limit.aclr.nr.cbandwidth.blimits.set(value = [PROPERTY_STRUCT_NAME](), channelBw = repcap.ChannelBw.Default, bandLimits = repcap.BandLimits.Default) \n
		Defines relative and absolute limits for the ACLR measured in an adjacent NR channel. The settings are defined separately
		for each channel bandwidth. \n
			:param structure: for set value, see the help for BlimitsStruct structure arguments.
			:param channelBw: optional repeated capability selector. Default value: Bw50 (settable in the interface 'Cbandwidth')
			:param bandLimits: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Blimits')"""
		channelBw_cmd_val = self._base.get_repcap_cmd_value(channelBw, repcap.ChannelBw)
		bandLimits_cmd_val = self._base.get_repcap_cmd_value(bandLimits, repcap.BandLimits)
		self._core.io.write_struct(f'CONFigure:NRMMw:MEASurement<Instance>:MEValuation:LIMit:ACLR:NR:CBANdwidth{channelBw_cmd_val}:BLIMits{bandLimits_cmd_val}', structure)

	def get(self, channelBw=repcap.ChannelBw.Default, bandLimits=repcap.BandLimits.Default) -> BlimitsStruct:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>:MEValuation:LIMit:ACLR:NR:CBANdwidth<bw>:BLIMits<n> \n
		Snippet: value: BlimitsStruct = driver.configure.nrMmwMeas.multiEval.limit.aclr.nr.cbandwidth.blimits.get(channelBw = repcap.ChannelBw.Default, bandLimits = repcap.BandLimits.Default) \n
		Defines relative and absolute limits for the ACLR measured in an adjacent NR channel. The settings are defined separately
		for each channel bandwidth. \n
			:param channelBw: optional repeated capability selector. Default value: Bw50 (settable in the interface 'Cbandwidth')
			:param bandLimits: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Blimits')
			:return: structure: for return value, see the help for BlimitsStruct structure arguments."""
		channelBw_cmd_val = self._base.get_repcap_cmd_value(channelBw, repcap.ChannelBw)
		bandLimits_cmd_val = self._base.get_repcap_cmd_value(bandLimits, repcap.BandLimits)
		return self._core.io.query_struct(f'CONFigure:NRMMw:MEASurement<Instance>:MEValuation:LIMit:ACLR:NR:CBANdwidth{channelBw_cmd_val}:BLIMits{bandLimits_cmd_val}?', self.__class__.BlimitsStruct())

	def clone(self) -> 'Blimits':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Blimits(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

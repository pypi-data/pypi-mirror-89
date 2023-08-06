from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DchType:
	"""DchType commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dchType", core, parent)

	# noinspection PyTypeChecker
	def fetch(self, carrierComponent=repcap.CarrierComponent.Default) -> enums.ChannelTypeA:
		"""SCPI: FETCh:NRMMw:MEASurement<Instance>:MEValuation[:CC<no>]:MODulation:DCHType \n
		Snippet: value: enums.ChannelTypeA = driver.nrMmwMeas.multiEval.cc.modulation.dchType.fetch(carrierComponent = repcap.CarrierComponent.Default) \n
		No command help available \n
		Suppressed linked return values: reliability \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: channel_type: No help available"""
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:NRMMw:MEASurement<Instance>:MEValuation:CC{carrierComponent_cmd_val}:MODulation:DCHType?', suppressed)
		return Conversions.str_to_scalar_enum(response, enums.ChannelTypeA)

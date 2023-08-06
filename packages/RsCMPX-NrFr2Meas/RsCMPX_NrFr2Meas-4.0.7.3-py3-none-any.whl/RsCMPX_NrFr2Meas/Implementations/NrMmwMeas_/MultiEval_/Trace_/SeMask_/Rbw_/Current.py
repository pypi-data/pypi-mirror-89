from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .......Internal.Types import DataType
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("current", core, parent)

	def read(self, rbw=repcap.Rbw.Default) -> List[float]:
		"""SCPI: READ:NRMMw:MEASurement<Instance>:MEValuation:TRACe:SEMask:RBW<kHz>:CURRent \n
		Snippet: value: List[float] = driver.nrMmwMeas.multiEval.trace.seMask.rbw.current.read(rbw = repcap.Rbw.Default) \n
		Returns the values of the spectrum emission traces. Separate traces are available for the individual resolution
		bandwidths (<kHz>) . The results of the current, average and maximum traces can be retrieved. See also 'Square Spectrum
		Emission Mask'. \n
		Suppressed linked return values: reliability \n
			:param rbw: optional repeated capability selector. Default value: Bw120 (settable in the interface 'Rbw')
			:return: power: Comma-separated list of power results The value in the middle of the result array corresponds to the center frequency. The test point separation between two results depends on the resolution bandwidth, see table below. For RBW1000, results are only available for frequencies with active limits using these RBWs. For other frequencies, INV is returned."""
		rbw_cmd_val = self._base.get_repcap_cmd_value(rbw, repcap.Rbw)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:NRMMw:MEASurement<Instance>:MEValuation:TRACe:SEMask:RBW{rbw_cmd_val}:CURRent?', suppressed)
		return response

	def fetch(self, rbw=repcap.Rbw.Default) -> List[float]:
		"""SCPI: FETCh:NRMMw:MEASurement<Instance>:MEValuation:TRACe:SEMask:RBW<kHz>:CURRent \n
		Snippet: value: List[float] = driver.nrMmwMeas.multiEval.trace.seMask.rbw.current.fetch(rbw = repcap.Rbw.Default) \n
		Returns the values of the spectrum emission traces. Separate traces are available for the individual resolution
		bandwidths (<kHz>) . The results of the current, average and maximum traces can be retrieved. See also 'Square Spectrum
		Emission Mask'. \n
		Suppressed linked return values: reliability \n
			:param rbw: optional repeated capability selector. Default value: Bw120 (settable in the interface 'Rbw')
			:return: power: Comma-separated list of power results The value in the middle of the result array corresponds to the center frequency. The test point separation between two results depends on the resolution bandwidth, see table below. For RBW1000, results are only available for frequencies with active limits using these RBWs. For other frequencies, INV is returned."""
		rbw_cmd_val = self._base.get_repcap_cmd_value(rbw, repcap.Rbw)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:NRMMw:MEASurement<Instance>:MEValuation:TRACe:SEMask:RBW{rbw_cmd_val}:CURRent?', suppressed)
		return response

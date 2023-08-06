from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dmodulation:
	"""Dmodulation commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dmodulation", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Seg_Reliability: int: Reliability indicator for the segment
			- Modulation: enums.ModScheme: π/2-BPSK, BPSK, QPSK, 16-QAM, 64-QAM, 256-QAM"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Seg_Reliability'),
			ArgStruct.scalar_enum('Modulation', enums.ModScheme)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Seg_Reliability: int = None
			self.Modulation: enums.ModScheme = None

	def fetch(self, sEGMent=repcap.SEGMent.Default) -> FetchStruct:
		"""SCPI: FETCh:NRMMw:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>:MODulation:DMODulation \n
		Snippet: value: FetchStruct = driver.nrMmwMeas.multiEval.listPy.segment.modulation.dmodulation.fetch(sEGMent = repcap.SEGMent.Default) \n
		Returns the detected modulation scheme for segment <no> in list mode. The result is determined from the last measured
		slot of the statistical length. \n
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		sEGMent_cmd_val = self._base.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		return self._core.io.query_struct(f'FETCh:NRMMw:MEASurement<Instance>:MEValuation:LIST:SEGMent{sEGMent_cmd_val}:MODulation:DMODulation?', self.__class__.FetchStruct())

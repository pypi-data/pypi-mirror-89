from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rlevel:
	"""Rlevel commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rlevel", core, parent)

	def get(self, sEGMent=repcap.SEGMent.Default) -> float:
		"""SCPI: SENSe:NRMMw:MEASurement<Instance>:LIST:SEGMent<no>:RLEVel \n
		Snippet: value: float = driver.sense.nrMmwMeas.listPy.segment.rlevel.get(sEGMent = repcap.SEGMent.Default) \n
		Queries the reference level of segment <no>. The reference level is calculated as Expected Nominal Power + User Margin. \n
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: level: Reference level of the segment"""
		sEGMent_cmd_val = self._base.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		response = self._core.io.query_str(f'SENSe:NRMMw:MEASurement<Instance>:LIST:SEGMent{sEGMent_cmd_val}:RLEVel?')
		return Conversions.str_to_float(response)

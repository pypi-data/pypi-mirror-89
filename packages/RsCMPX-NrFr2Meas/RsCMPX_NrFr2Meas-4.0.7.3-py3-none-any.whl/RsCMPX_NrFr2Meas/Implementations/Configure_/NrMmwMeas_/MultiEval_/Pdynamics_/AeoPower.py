from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AeoPower:
	"""AeoPower commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("aeoPower", core, parent)

	def get_leading(self) -> int:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>:MEValuation:PDYNamics:AEOPower:LEADing \n
		Snippet: value: int = driver.configure.nrMmwMeas.multiEval.pdynamics.aeoPower.get_leading() \n
		No command help available \n
			:return: leading: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRMMw:MEASurement<Instance>:MEValuation:PDYNamics:AEOPower:LEADing?')
		return Conversions.str_to_int(response)

	def set_leading(self, leading: int) -> None:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>:MEValuation:PDYNamics:AEOPower:LEADing \n
		Snippet: driver.configure.nrMmwMeas.multiEval.pdynamics.aeoPower.set_leading(leading = 1) \n
		No command help available \n
			:param leading: No help available
		"""
		param = Conversions.decimal_value_to_str(leading)
		self._core.io.write(f'CONFigure:NRMMw:MEASurement<Instance>:MEValuation:PDYNamics:AEOPower:LEADing {param}')

	def get_lagging(self) -> int:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>:MEValuation:PDYNamics:AEOPower:LAGGing \n
		Snippet: value: int = driver.configure.nrMmwMeas.multiEval.pdynamics.aeoPower.get_lagging() \n
		No command help available \n
			:return: lagging: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRMMw:MEASurement<Instance>:MEValuation:PDYNamics:AEOPower:LAGGing?')
		return Conversions.str_to_int(response)

	def set_lagging(self, lagging: int) -> None:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>:MEValuation:PDYNamics:AEOPower:LAGGing \n
		Snippet: driver.configure.nrMmwMeas.multiEval.pdynamics.aeoPower.set_lagging(lagging = 1) \n
		No command help available \n
			:param lagging: No help available
		"""
		param = Conversions.decimal_value_to_str(lagging)
		self._core.io.write(f'CONFigure:NRMMw:MEASurement<Instance>:MEValuation:PDYNamics:AEOPower:LAGGing {param}')

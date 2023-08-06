from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UlDl:
	"""UlDl commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ulDl", core, parent)

	@property
	def pattern(self):
		"""pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .UlDl_.Pattern import Pattern
			self._pattern = Pattern(self._core, self._base)
		return self._pattern

	# noinspection PyTypeChecker
	def get_periodicity(self) -> enums.Periodicity:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>:ULDL:PERiodicity \n
		Snippet: value: enums.Periodicity = driver.configure.nrMmwMeas.ulDl.get_periodicity() \n
		Configures the periodicity of the UL-DL pattern. \n
			:return: periodicity: 0.5 ms, 0.625 ms, 1 ms, 1.25 ms, 2 ms, 2.5 ms, 5 ms, 10 ms
		"""
		response = self._core.io.query_str('CONFigure:NRMMw:MEASurement<Instance>:ULDL:PERiodicity?')
		return Conversions.str_to_scalar_enum(response, enums.Periodicity)

	def set_periodicity(self, periodicity: enums.Periodicity) -> None:
		"""SCPI: CONFigure:NRMMw:MEASurement<Instance>:ULDL:PERiodicity \n
		Snippet: driver.configure.nrMmwMeas.ulDl.set_periodicity(periodicity = enums.Periodicity.MS05) \n
		Configures the periodicity of the UL-DL pattern. \n
			:param periodicity: 0.5 ms, 0.625 ms, 1 ms, 1.25 ms, 2 ms, 2.5 ms, 5 ms, 10 ms
		"""
		param = Conversions.enum_scalar_to_str(periodicity, enums.Periodicity)
		self._core.io.write(f'CONFigure:NRMMw:MEASurement<Instance>:ULDL:PERiodicity {param}')

	def clone(self) -> 'UlDl':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = UlDl(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

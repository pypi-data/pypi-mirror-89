from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nrpm:
	"""Nrpm commands group definition. 4 total commands, 1 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nrpm", core, parent)

	@property
	def sensor(self):
		"""sensor commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sensor'):
			from .Nrpm_.Sensor import Sensor
			self._sensor = Sensor(self._core, self._base)
		return self._sensor

	def get_scount(self) -> int:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRPM:SCOunt \n
		Snippet: value: int = driver.configure.nrpm.get_scount() \n
		No command help available \n
			:return: statistic_count: No help available
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:NRPM:SCOunt?')
		return Conversions.str_to_int(response)

	def set_scount(self, statistic_count: int) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRPM:SCOunt \n
		Snippet: driver.configure.nrpm.set_scount(statistic_count = 1) \n
		No command help available \n
			:param statistic_count: No help available
		"""
		param = Conversions.decimal_value_to_str(statistic_count)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:NRPM:SCOunt {param}')

	# noinspection PyTypeChecker
	def get_repetition(self) -> enums.Repeat:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRPM:REPetition \n
		Snippet: value: enums.Repeat = driver.configure.nrpm.get_repetition() \n
		No command help available \n
			:return: repetition: No help available
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:NRPM:REPetition?')
		return Conversions.str_to_scalar_enum(response, enums.Repeat)

	def set_repetition(self, repetition: enums.Repeat) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRPM:REPetition \n
		Snippet: driver.configure.nrpm.set_repetition(repetition = enums.Repeat.CONTinuous) \n
		No command help available \n
			:param repetition: No help available
		"""
		param = Conversions.enum_scalar_to_str(repetition, enums.Repeat)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:NRPM:REPetition {param}')

	def get_timeout(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRPM:TOUT \n
		Snippet: value: float = driver.configure.nrpm.get_timeout() \n
		No command help available \n
			:return: tcd_time_out: No help available
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:NRPM:TOUT?')
		return Conversions.str_to_float(response)

	def set_timeout(self, tcd_time_out: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRPM:TOUT \n
		Snippet: driver.configure.nrpm.set_timeout(tcd_time_out = 1.0) \n
		No command help available \n
			:param tcd_time_out: No help available
		"""
		param = Conversions.decimal_value_to_str(tcd_time_out)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:NRPM:TOUT {param}')

	def clone(self) -> 'Nrpm':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Nrpm(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

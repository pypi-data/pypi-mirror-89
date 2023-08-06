from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Types import DataType
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Slength:
	"""Slength commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("slength", core, parent)

	def set(self, index: int, step_length: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:POWer:PSET:SLENgth \n
		Snippet: driver.configure.power.parameterSetList.slength.set(index = 1, step_length = 1.0) \n
		Selects the time between the beginning of two consecutive measured power steps for a particular parameter set <Index>. \n
			:param index: Number of the parameter set Range: 0 to 31
			:param step_length: Range: 50E-6 s to 1 s, Unit: s
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('index', index, DataType.Integer), ArgSingle('step_length', step_length, DataType.Float))
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:POWer:PSET:SLENgth {param}'.rstrip())

	def get(self, index: int) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:POWer:PSET:SLENgth \n
		Snippet: value: float = driver.configure.power.parameterSetList.slength.get(index = 1) \n
		Selects the time between the beginning of two consecutive measured power steps for a particular parameter set <Index>. \n
			:param index: Number of the parameter set Range: 0 to 31
			:return: step_length: Range: 50E-6 s to 1 s, Unit: s"""
		param = Conversions.decimal_value_to_str(index)
		response = self._core.io.query_str(f'CONFigure:GPRF:MEASurement<Instance>:POWer:PSET:SLENgth? {param}')
		return Conversions.str_to_float(response)

	def get_all(self) -> List[float]:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:POWer:PSET:SLENgth:ALL \n
		Snippet: value: List[float] = driver.configure.power.parameterSetList.slength.get_all() \n
		Selects the time between the beginning of two consecutive measured power steps for all parameter sets. \n
			:return: step_length: Comma-separated list of 32 values, for parameter set no. 0 to 31 Range: 50E-6 s to 1 s, Unit: s
		"""
		response = self._core.io.query_bin_or_ascii_float_list('CONFigure:GPRF:MEASurement<Instance>:POWer:PSET:SLENgth:ALL?')
		return response

	def set_all(self, step_length: List[float]) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:POWer:PSET:SLENgth:ALL \n
		Snippet: driver.configure.power.parameterSetList.slength.set_all(step_length = [1.1, 2.2, 3.3]) \n
		Selects the time between the beginning of two consecutive measured power steps for all parameter sets. \n
			:param step_length: Comma-separated list of 32 values, for parameter set no. 0 to 31 Range: 50E-6 s to 1 s, Unit: s
		"""
		param = Conversions.list_to_csv_str(step_length)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:POWer:PSET:SLENgth:ALL {param}')

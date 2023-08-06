from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Types import DataType
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bandwidth:
	"""Bandwidth commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bandwidth", core, parent)

	def set(self, index: int, bandwidth: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:POWer:PSET:FILTer:BANDpass:BWIDth \n
		Snippet: driver.configure.power.parameterSetList.filterPy.bandpass.bandwidth.set(index = 1, bandwidth = 1.0) \n
		Selects the bandpass filter bandwidth for a particular parameter set <Index>. \n
			:param index: Number of the parameter set Range: 0 to 31
			:param bandwidth: Only certain values within the allowed range can be configured. Values in-between can be entered but are rounded to allowed values. For a list of the supported values, see method RsCmwGprfMeas.Configure.Power.FilterPy.Bandpass.bandwidth. Range: 1 kHz to 160 MHz, Unit: Hz
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('index', index, DataType.Integer), ArgSingle('bandwidth', bandwidth, DataType.Float))
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:POWer:PSET:FILTer:BANDpass:BWIDth {param}'.rstrip())

	def get(self, index: int) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:POWer:PSET:FILTer:BANDpass:BWIDth \n
		Snippet: value: float = driver.configure.power.parameterSetList.filterPy.bandpass.bandwidth.get(index = 1) \n
		Selects the bandpass filter bandwidth for a particular parameter set <Index>. \n
			:param index: Number of the parameter set Range: 0 to 31
			:return: bandwidth: Only certain values within the allowed range can be configured. Values in-between can be entered but are rounded to allowed values. For a list of the supported values, see method RsCmwGprfMeas.Configure.Power.FilterPy.Bandpass.bandwidth. Range: 1 kHz to 160 MHz, Unit: Hz"""
		param = Conversions.decimal_value_to_str(index)
		response = self._core.io.query_str(f'CONFigure:GPRF:MEASurement<Instance>:POWer:PSET:FILTer:BANDpass:BWIDth? {param}')
		return Conversions.str_to_float(response)

	def get_all(self) -> List[float]:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:POWer:PSET:FILTer:BANDpass:BWIDth:ALL \n
		Snippet: value: List[float] = driver.configure.power.parameterSetList.filterPy.bandpass.bandwidth.get_all() \n
		Selects the bandpass filter bandwidth for all parameter sets. \n
			:return: bandwidth: Comma-separated list of 32 values, for parameter set no. 0 to 31 Only certain values within the allowed range can be configured. Values in-between can be entered but are rounded to allowed values. For a list of the supported values, see method RsCmwGprfMeas.Configure.Power.FilterPy.Bandpass.bandwidth. Range: 1 kHz to 160 MHz, Unit: Hz
		"""
		response = self._core.io.query_bin_or_ascii_float_list('CONFigure:GPRF:MEASurement<Instance>:POWer:PSET:FILTer:BANDpass:BWIDth:ALL?')
		return response

	def set_all(self, bandwidth: List[float]) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:POWer:PSET:FILTer:BANDpass:BWIDth:ALL \n
		Snippet: driver.configure.power.parameterSetList.filterPy.bandpass.bandwidth.set_all(bandwidth = [1.1, 2.2, 3.3]) \n
		Selects the bandpass filter bandwidth for all parameter sets. \n
			:param bandwidth: Comma-separated list of 32 values, for parameter set no. 0 to 31 Only certain values within the allowed range can be configured. Values in-between can be entered but are rounded to allowed values. For a list of the supported values, see method RsCmwGprfMeas.Configure.Power.FilterPy.Bandpass.bandwidth. Range: 1 kHz to 160 MHz, Unit: Hz
		"""
		param = Conversions.list_to_csv_str(bandwidth)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:POWer:PSET:FILTer:BANDpass:BWIDth:ALL {param}')

from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("current", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:GPRF:MEASurement<Instance>:SPECtrum:RMS:CURRent \n
		Snippet: value: List[float] = driver.spectrum.rms.current.fetch() \n
		Returns the traces calculated with the RMS detector. Current, average, maximum and minimum traces can be retrieved. \n
		Use RsCmwGprfMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: power: 1001 values Range: -150 dBm to 50 dBm, Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:GPRF:MEASurement<Instance>:SPECtrum:RMS:CURRent?', suppressed)
		return response

	def read(self) -> List[float]:
		"""SCPI: READ:GPRF:MEASurement<Instance>:SPECtrum:RMS:CURRent \n
		Snippet: value: List[float] = driver.spectrum.rms.current.read() \n
		Returns the traces calculated with the RMS detector. Current, average, maximum and minimum traces can be retrieved. \n
		Use RsCmwGprfMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: power: 1001 values Range: -150 dBm to 50 dBm, Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:GPRF:MEASurement<Instance>:SPECtrum:RMS:CURRent?', suppressed)
		return response

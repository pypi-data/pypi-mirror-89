from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Npeak:
	"""Npeak commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("npeak", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: See 'Reliability Indicator'
			- Xvalue: float: X value
			- Yvalue: float: Y value Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Xvalue'),
			ArgStruct.scalar_float('Yvalue')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Xvalue: float = None
			self.Yvalue: float = None

	def fetch(self, detector: enums.Detector, statistic: enums.Statistic) -> FetchStruct:
		"""SCPI: FETCh:GPRF:MEASurement<Instance>:SPECtrum:REFMarker:NPEak \n
		Snippet: value: FetchStruct = driver.spectrum.referenceMarker.npeak.fetch(detector = enums.Detector.AUTopeak, statistic = enums.Statistic.AVERage) \n
		Moves the reference marker to the next lower (or equal) peak, relative to the current marker position. Returns the X and
		Y value of the new marker position. The trace is selected by <Detector> and <Statistic>. \n
			:param detector: AVERage | RMS | SAMPle | MINPeak | MAXPeak | AUTopeak Selects the detector type, see 'Detector hotkey'.
			:param statistic: CURRent | AVERage | MAXimum | MINimum
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		param = ArgSingleList().compose_cmd_string(ArgSingle('detector', detector, DataType.Enum), ArgSingle('statistic', statistic, DataType.Enum))
		return self._core.io.query_struct(f'FETCh:GPRF:MEASurement<Instance>:SPECtrum:REFMarker:NPEak? {param}'.rstrip(), self.__class__.FetchStruct())

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from .... import enums
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("power", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: No parameter help available
			- Power_Antenna_1: float: No parameter help available
			- Power_Antenna_2: float: No parameter help available
			- Power_Antenna_3: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Power_Antenna_1'),
			ArgStruct.scalar_float('Power_Antenna_2'),
			ArgStruct.scalar_float('Power_Antenna_3')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Power_Antenna_1: float = None
			self.Power_Antenna_2: float = None
			self.Power_Antenna_3: float = None

	def read(self, sensor=repcap.Sensor.Default) -> ResultData:
		"""SCPI: READ:GPRF:MEASurement<Instance>:NRPM:SENSor<nr_NRPM>:POWer \n
		Snippet: value: ResultData = driver.nrpm.sensor.power.read(sensor = repcap.Sensor.Default) \n
		No command help available \n
			:param sensor: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sensor')
			:return: structure: for return value, see the help for ResultData structure arguments."""
		sensor_cmd_val = self._base.get_repcap_cmd_value(sensor, repcap.Sensor)
		return self._core.io.query_struct(f'READ:GPRF:MEASurement<Instance>:NRPM:SENSor{sensor_cmd_val}:POWer?', self.__class__.ResultData())

	def fetch(self, sensor=repcap.Sensor.Default) -> ResultData:
		"""SCPI: FETCh:GPRF:MEASurement<Instance>:NRPM:SENSor<nr_NRPM>:POWer \n
		Snippet: value: ResultData = driver.nrpm.sensor.power.fetch(sensor = repcap.Sensor.Default) \n
		No command help available \n
			:param sensor: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sensor')
			:return: structure: for return value, see the help for ResultData structure arguments."""
		sensor_cmd_val = self._base.get_repcap_cmd_value(sensor, repcap.Sensor)
		return self._core.io.query_struct(f'FETCh:GPRF:MEASurement<Instance>:NRPM:SENSor{sensor_cmd_val}:POWer?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: No parameter help available
			- State_Antenna_1: float: No parameter help available
			- State_Antenna_2: enums.ResultStatus2: No parameter help available
			- State_Antenna_3: enums.ResultStatus2: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('State_Antenna_1'),
			ArgStruct.scalar_enum('State_Antenna_2', enums.ResultStatus2),
			ArgStruct.scalar_enum('State_Antenna_3', enums.ResultStatus2)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.State_Antenna_1: float = None
			self.State_Antenna_2: enums.ResultStatus2 = None
			self.State_Antenna_3: enums.ResultStatus2 = None

	def calculate(self, sensor=repcap.Sensor.Default) -> CalculateStruct:
		"""SCPI: CALCulate:GPRF:MEASurement<Instance>:NRPM:SENSor<nr_NRPM>:POWer \n
		Snippet: value: CalculateStruct = driver.nrpm.sensor.power.calculate(sensor = repcap.Sensor.Default) \n
		No command help available \n
			:param sensor: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sensor')
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		sensor_cmd_val = self._base.get_repcap_cmd_value(sensor, repcap.Sensor)
		return self._core.io.query_struct(f'CALCulate:GPRF:MEASurement<Instance>:NRPM:SENSor{sensor_cmd_val}:POWer?', self.__class__.CalculateStruct())

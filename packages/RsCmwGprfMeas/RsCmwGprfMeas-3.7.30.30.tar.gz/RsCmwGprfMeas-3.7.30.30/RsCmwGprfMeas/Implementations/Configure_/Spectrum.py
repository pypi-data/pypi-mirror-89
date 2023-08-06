from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Spectrum:
	"""Spectrum commands group definition. 22 total commands, 3 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("spectrum", core, parent)

	@property
	def zeroSpan(self):
		"""zeroSpan commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_zeroSpan'):
			from .Spectrum_.ZeroSpan import ZeroSpan
			self._zeroSpan = ZeroSpan(self._core, self._base)
		return self._zeroSpan

	@property
	def frequency(self):
		"""frequency commands group. 1 Sub-classes, 4 commands."""
		if not hasattr(self, '_frequency'):
			from .Spectrum_.Frequency import Frequency
			self._frequency = Frequency(self._core, self._base)
		return self._frequency

	@property
	def freqSweep(self):
		"""freqSweep commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_freqSweep'):
			from .Spectrum_.FreqSweep import FreqSweep
			self._freqSweep = FreqSweep(self._core, self._base)
		return self._freqSweep

	# noinspection PyTypeChecker
	def get_amode(self) -> enums.AveragingMode:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:AMODe \n
		Snippet: value: enums.AveragingMode = driver.configure.spectrum.get_amode() \n
		Defines how the R&S CMW calculates the AVERage traces from the current results. \n
			:return: averaging_mode: LINear | LOGarithmic
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:SPECtrum:AMODe?')
		return Conversions.str_to_scalar_enum(response, enums.AveragingMode)

	def set_amode(self, averaging_mode: enums.AveragingMode) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:AMODe \n
		Snippet: driver.configure.spectrum.set_amode(averaging_mode = enums.AveragingMode.LINear) \n
		Defines how the R&S CMW calculates the AVERage traces from the current results. \n
			:param averaging_mode: LINear | LOGarithmic
		"""
		param = Conversions.enum_scalar_to_str(averaging_mode, enums.AveragingMode)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:AMODe {param}')

	# noinspection PyTypeChecker
	def get_repetition(self) -> enums.Repeat:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:REPetition \n
		Snippet: value: enums.Repeat = driver.configure.spectrum.get_repetition() \n
		Specifies the repetition mode of the measurement. The repetition mode specifies whether the measurement is stopped after
		a single shot or repeated continuously. Use CONFigure:..:MEAS<i>:...:SCOunt to determine the number of measurement
		intervals per single shot. \n
			:return: repetition: SINGleshot | CONTinuous SINGleshot: single-shot measurement CONTinuous: continuous measurement
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:SPECtrum:REPetition?')
		return Conversions.str_to_scalar_enum(response, enums.Repeat)

	def set_repetition(self, repetition: enums.Repeat) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:REPetition \n
		Snippet: driver.configure.spectrum.set_repetition(repetition = enums.Repeat.CONTinuous) \n
		Specifies the repetition mode of the measurement. The repetition mode specifies whether the measurement is stopped after
		a single shot or repeated continuously. Use CONFigure:..:MEAS<i>:...:SCOunt to determine the number of measurement
		intervals per single shot. \n
			:param repetition: SINGleshot | CONTinuous SINGleshot: single-shot measurement CONTinuous: continuous measurement
		"""
		param = Conversions.enum_scalar_to_str(repetition, enums.Repeat)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:REPetition {param}')

	def get_timeout(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:TOUT \n
		Snippet: value: float = driver.configure.spectrum.get_timeout() \n
		Defines a timeout for the measurement. The timer is started when the measurement is initiated via a READ or INIT command.
		It is not started if the measurement is initiated manually ([ON | OFF] key or [RESTART | STOP] key) .
		When the measurement has completed the first measurement cycle (first single shot) , the statistical depth is reached and
		the timer is reset. If the first measurement cycle has not been completed when the timer expires, the measurement is
		stopped. The measurement state changes to RDY. The reliability indicator is set to 1, indicating that a measurement
		timeout occurred. Still running READ, FETCh or CALCulate commands are completed, returning the available results.
		At least for some results, there are no values at all or the statistical depth has not been reached. A timeout of 0 s
		corresponds to an infinite measurement timeout. \n
			:return: tcd_time_out: Unit: s
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:SPECtrum:TOUT?')
		return Conversions.str_to_float(response)

	def set_timeout(self, tcd_time_out: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:TOUT \n
		Snippet: driver.configure.spectrum.set_timeout(tcd_time_out = 1.0) \n
		Defines a timeout for the measurement. The timer is started when the measurement is initiated via a READ or INIT command.
		It is not started if the measurement is initiated manually ([ON | OFF] key or [RESTART | STOP] key) .
		When the measurement has completed the first measurement cycle (first single shot) , the statistical depth is reached and
		the timer is reset. If the first measurement cycle has not been completed when the timer expires, the measurement is
		stopped. The measurement state changes to RDY. The reliability indicator is set to 1, indicating that a measurement
		timeout occurred. Still running READ, FETCh or CALCulate commands are completed, returning the available results.
		At least for some results, there are no values at all or the statistical depth has not been reached. A timeout of 0 s
		corresponds to an infinite measurement timeout. \n
			:param tcd_time_out: Unit: s
		"""
		param = Conversions.decimal_value_to_str(tcd_time_out)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:TOUT {param}')

	def get_scount(self) -> int:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:SCOunt \n
		Snippet: value: int = driver.configure.spectrum.get_scount() \n
		Specifies the statistic count of the measurement. The statistic count is equal to the number of measurement intervals per
		single shot. \n
			:return: statistic_count: Number of measurement intervals. A measurement interval comprises a single frequency sweep. Range: 1 to 1000
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:SPECtrum:SCOunt?')
		return Conversions.str_to_int(response)

	def set_scount(self, statistic_count: int) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:SCOunt \n
		Snippet: driver.configure.spectrum.set_scount(statistic_count = 1) \n
		Specifies the statistic count of the measurement. The statistic count is equal to the number of measurement intervals per
		single shot. \n
			:param statistic_count: Number of measurement intervals. A measurement interval comprises a single frequency sweep. Range: 1 to 1000
		"""
		param = Conversions.decimal_value_to_str(statistic_count)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:SCOunt {param}')

	def clone(self) -> 'Spectrum':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Spectrum(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

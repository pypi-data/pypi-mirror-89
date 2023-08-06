from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bandpass:
	"""Bandpass commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bandpass", core, parent)

	def get_bandwidth(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:FILTer:BANDpass:BWIDth \n
		Snippet: value: float = driver.configure.iqRecorder.filterPy.bandpass.get_bandwidth() \n
		Selects the bandwidth for a bandpass filter. \n
			:return: band_pass_bw: 1 kHz | 10 kHz | 100 kHz | 1 MHz | 10 MHz | 40 MHz | 160 MHz Values in-between are rounded. Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:IQRecorder:FILTer:BANDpass:BWIDth?')
		return Conversions.str_to_float(response)

	def set_bandwidth(self, band_pass_bw: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:FILTer:BANDpass:BWIDth \n
		Snippet: driver.configure.iqRecorder.filterPy.bandpass.set_bandwidth(band_pass_bw = 1.0) \n
		Selects the bandwidth for a bandpass filter. \n
			:param band_pass_bw: 1 kHz | 10 kHz | 100 kHz | 1 MHz | 10 MHz | 40 MHz | 160 MHz Values in-between are rounded. Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(band_pass_bw)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:IQRecorder:FILTer:BANDpass:BWIDth {param}')

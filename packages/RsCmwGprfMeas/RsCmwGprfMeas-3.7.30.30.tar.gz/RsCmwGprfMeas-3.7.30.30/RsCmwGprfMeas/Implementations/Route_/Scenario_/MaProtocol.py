from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MaProtocol:
	"""MaProtocol commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("maProtocol", core, parent)

	def set(self, controler: str = None, converter: enums.RxConverter = None) -> None:
		"""SCPI: ROUTe:GPRF:MEASurement<Instance>:SCENario:MAPRotocol \n
		Snippet: driver.route.scenario.maProtocol.set(controler = '1', converter = enums.RxConverter.IRX1) \n
		No command help available \n
			:param controler: No help available
			:param converter: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('controler', controler, DataType.String, True), ArgSingle('converter', converter, DataType.Enum, True))
		self._core.io.write(f'ROUTe:GPRF:MEASurement<Instance>:SCENario:MAPRotocol {param}'.rstrip())

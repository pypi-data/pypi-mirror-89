from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Catalog:
	"""Catalog commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("catalog", core, parent)

	def get_cspath(self) -> List[str]:
		"""SCPI: ROUTe:GPRF:MEASurement<Instance>:SCENario:CATalog:CSPath \n
		Snippet: value: List[str] = driver.route.scenario.catalog.get_cspath() \n
		Queries the possible master firmware applications for a combined signal path scenario. The returned list contains all
		installed signaling applications. \n
			:return: csp_masters: Comma-separated list of string parameters For example '1xEV-DO Sig1', 'GSM Sig2' 'No Connection' means that no signaling application is installed.
		"""
		response = self._core.io.query_str('ROUTe:GPRF:MEASurement<Instance>:SCENario:CATalog:CSPath?')
		return Conversions.str_to_str_list(response)

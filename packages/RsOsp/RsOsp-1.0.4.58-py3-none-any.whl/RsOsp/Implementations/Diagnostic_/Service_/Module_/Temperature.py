from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Temperature:
	"""Temperature commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("temperature", core, parent)

	def get(self, modules: str) -> List[float]:
		"""SCPI: DIAGnostic:SERVice:MODule:TEMPerature \n
		Snippet: value: List[float] = driver.diagnostic.service.module.temperature.get(modules = r1) \n
		No command help available \n
			:param modules: No help available
			:return: temperature_value: No help available"""
		param = Conversions.value_to_str(modules)
		response = self._core.io.query_bin_or_ascii_float_list(f'DIAGnostic:SERVice:MODule:TEMPerature? {param}')
		return response

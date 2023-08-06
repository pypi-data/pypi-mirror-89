from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bbin:
	"""Bbin commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bbin", core, parent)

	def get_rb_error(self) -> bool:
		"""SCPI: TEST<HW>:BBIN:RBERror \n
		Snippet: value: bool = driver.test.bbin.get_rb_error() \n
		No command help available \n
			:return: rb_error: No help available
		"""
		response = self._core.io.query_str('TEST<HwInstance>:BBIN:RBERror?')
		return Conversions.str_to_bool(response)

	def get_value(self) -> bool:
		"""SCPI: TEST:BBIN \n
		Snippet: value: bool = driver.test.bbin.get_value() \n
		This command performs a selftest on the baseband input hardware options. Several analog diagnostics points are checked to
		verify the correct function of the module. \n
			:return: bbin: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('TEST:BBIN?')
		return Conversions.str_to_bool(response)

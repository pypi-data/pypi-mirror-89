from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Connector:
	"""Connector commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("connector", core, parent)

	def get_auxio(self) -> bool:
		"""SCPI: TEST:CONNector:AUXio \n
		Snippet: value: bool = driver.test.connector.get_auxio() \n
		No command help available \n
			:return: aux_io: No help available
		"""
		response = self._core.io.query_str('TEST:CONNector:AUXio?')
		return Conversions.str_to_bool(response)

	def get_bnc(self) -> bool:
		"""SCPI: TEST:CONNector:BNC \n
		Snippet: value: bool = driver.test.connector.get_bnc() \n
		No command help available \n
			:return: bnc: No help available
		"""
		response = self._core.io.query_str('TEST:CONNector:BNC?')
		return Conversions.str_to_bool(response)

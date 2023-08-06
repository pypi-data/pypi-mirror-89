from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Res:
	"""Res commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("res", core, parent)

	# noinspection PyTypeChecker
	def get_color(self) -> enums.Colour:
		"""SCPI: TEST:RES:COLor \n
		Snippet: value: enums.Colour = driver.test.res.get_color() \n
		No command help available \n
			:return: color: No help available
		"""
		response = self._core.io.query_str('TEST:RES:COLor?')
		return Conversions.str_to_scalar_enum(response, enums.Colour)

	def set_color(self, color: enums.Colour) -> None:
		"""SCPI: TEST:RES:COLor \n
		Snippet: driver.test.res.set_color(color = enums.Colour.GREen) \n
		No command help available \n
			:param color: No help available
		"""
		param = Conversions.enum_scalar_to_str(color, enums.Colour)
		self._core.io.write(f'TEST:RES:COLor {param}')

	def get_wind(self) -> bool:
		"""SCPI: TEST:RES:WIND \n
		Snippet: value: bool = driver.test.res.get_wind() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('TEST:RES:WIND?')
		return Conversions.str_to_bool(response)

	def set_wind(self, state: bool) -> None:
		"""SCPI: TEST:RES:WIND \n
		Snippet: driver.test.res.set_wind(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'TEST:RES:WIND {param}')

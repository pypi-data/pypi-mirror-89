from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PciExpress:
	"""PciExpress commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pciExpress", core, parent)

	def get_resource(self) -> str:
		"""SCPI: SYSTem:COMMunicate:PCIexpress:RESource \n
		Snippet: value: str = driver.system.communicate.pciExpress.get_resource() \n
		Queries the visa resource string for remote control via the PCIe interface. \n
			:return: resource: string
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:PCIexpress:RESource?')
		return trim_str_response(response)

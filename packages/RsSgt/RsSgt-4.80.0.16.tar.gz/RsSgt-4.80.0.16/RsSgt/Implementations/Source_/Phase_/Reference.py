from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Reference:
	"""Reference commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("reference", core, parent)

	def set(self) -> None:
		"""SCPI: [SOURce<HW>]:PHASe:REFerence \n
		Snippet: driver.source.phase.reference.set() \n
		Adopts the phase set with command method RsSgt.Source.Phase.value as the current phase. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:PHASe:REFerence')

	def set_with_opc(self) -> None:
		"""SCPI: [SOURce<HW>]:PHASe:REFerence \n
		Snippet: driver.source.phase.reference.set_with_opc() \n
		Adopts the phase set with command method RsSgt.Source.Phase.value as the current phase. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSgt.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:PHASe:REFerence')

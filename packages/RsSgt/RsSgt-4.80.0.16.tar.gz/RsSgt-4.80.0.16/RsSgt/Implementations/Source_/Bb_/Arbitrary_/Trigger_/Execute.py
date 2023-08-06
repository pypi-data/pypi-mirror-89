from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Execute:
	"""Execute commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("execute", core, parent)

	def set(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:TRIGger:EXECute \n
		Snippet: driver.source.bb.arbitrary.trigger.execute.set() \n
		The command executes a trigger. The internal trigger source must be selected using the command ARB:TRIGger:SOURce
		INTernal and a trigger mode other than AUTO must be selected using the command ARB:SEQuence. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:TRIGger:EXECute')

	def set_with_opc(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:TRIGger:EXECute \n
		Snippet: driver.source.bb.arbitrary.trigger.execute.set_with_opc() \n
		The command executes a trigger. The internal trigger source must be selected using the command ARB:TRIGger:SOURce
		INTernal and a trigger mode other than AUTO must be selected using the command ARB:SEQuence. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSgt.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:ARBitrary:TRIGger:EXECute')
